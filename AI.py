# Class AI (a possible extra attribute could be "policy")

# METODS
#
# action 
# S_a_r_S_prime
# fill_memory
# reset_memory
# update_memory
# test
# train
#

import numpy as np
import random 
import copy

from board import *

class AI:
    def __init__(self, whichPlayer, NN, epsilon, memorySize):
        self.whichPlayer = whichPlayer
        self.NN = NN
        self.epsilon = epsilon
        self.memorySize = memorySize
        self.memory = []
        self.reward = {
            "win":10,
            "lose":-10,
            "draw":0.5,
            "none":0
        }


    def action(self, board):
    	# first check if this is the right player
        if self.whichPlayer == board.playerToPlay:
        	# action following the epsilon-greedy policy
        	# the agent plays randomly with probability epsilon
            if random.random() < self.epsilon:
                column = random.choice(board.actions_available())
                board.move(column)
            # the agent plays greedly (w.r.t. the NN) with prob 1-epsilon
            else:
                actionValues = self.NN.evaluate(board.matrix)	
                # first we need to create a mask before applying argmax
                mask = np.ones(actionValues.size, dtype=bool)
                mask[board.actions_available()] = False
                maskedActionValues = np.ma.array(actionValues, mask=mask)
                column = np.argmax(maskedActionValues)
                board.move(column)
            return column
        else:
            print("\nERROR!!!\nThis agent is a player ", self.whichPlayer, "and is trying")
            print("to play as player", board.playerToPlay,".\n")


    def S_a_r_S_prime(self, board, environment):
    	# !!! WARNING !!! board is supposed to be an instance of Board class
    	# and environment is supposed to be an instance of AI class !!!
    	# This method make the AI play 1 turn.
    	# The agent starts in state S (board where the agent has to play)
    	# plays a move a (from the available actions), 
    	# gets a reward r and it is sent in the new state S_prime 
    	# (namely the environment, i.e. the other player, plays a move).
        S = copy.deepcopy(board.matrix)  
        # the agent plays
        self.action(board)
        a = copy.deepcopy(board.lastMove)
        if board.is_winning() == True:
            r = self.reward["win"]
            board.reset(self, environment)
            S_prime = copy.deepcopy(board.matrix)
        elif board.is_full() == True:
            r = self.reward["draw"]
            board.reset(self, environment)
            S_prime = copy.deepcopy(board.matrix)
        else:
        	# environment plays
            environment.action(board)
            S_prime = copy.deepcopy(board.matrix)
            if board.is_winning() == True:
                r = self.reward["lose"]
                board.reset(self, environment)
            elif (board.is_winning() == False) and (board.is_full() == True):
                r = self.reward["draw"]
                board.reset(self, environment)
            else:
                r = self.reward["none"]
        experience = [S,a,r,S_prime]
        return experience


    def fill_memory(self, environment):
    	# this method creates the memory of the agent
        board = empty_board(self.NN.nRows, self.NN.nColumns)
        board.reset(self, environment)
        memory = list([])
        while len(self.memory) < self.memorySize:
            experience = self.S_a_r_S_prime(board, environment)
            self.memory.append(experience)


    def reset_memory(self):
        self.memory = []
        return


    def update_memory(self, experience):
    	# if the memory is empty then there is a problem!
        if len(self.memory) == 0:
            print("\nERROR! Trying to update memory, but memory is empty!!!\n")
        else:
            # otherwise remove a random experience element from the memory
            self.memory.pop(random.choice(range(len(self.memory))))
            # and add the fresh experience element to the memory
            self.memory.append(experience)
            

    def get_batch(self, batchSize = 10):
        if batchSize <= len(self.memory):
            batch = random.sample(self.memory, batchSize)
        else:
        	# if the batchSize is bigger then the memory length then something is wrong
            print("\nERROR!!! Trying to get a batch from memory, but the batch size is bigger than the memory length.\n")
        return batch


    def test(self, environment, nMoves = 1000, randomEnvironment=False):
    	# initialize the counter
        winCounter = 0
        loseCounter = 0
        drawCounter = 0
        # let's save the value of the epsilons
        epsilonAgent = copy.copy(self.epsilon)
        epsilonEnvironment = copy.copy(environment.epsilon)
        # let's make the agent act greedly
        self.epsilon = 0
        if randomEnvironment == True:
            environment.epsilon = 1
        else:
            environment.epsilon = 0
        # initialize board
        board = empty_board(self.NN.nRows, self.NN.nColumns)
        board.reset(self, environment)
        for move in range(nMoves):
            [S,a,r,S_prime] = self.S_a_r_S_prime(board, environment)
            if r == self.reward["win"]:
            	winCounter = winCounter + 1
            elif r == self.reward["lose"]:
                loseCounter = loseCounter + 1
            elif r == self.reward["draw"]:
            	drawCounter = drawCounter + 1
        # frequencies
        winFrequency = round((winCounter*100)/(loseCounter + drawCounter + winCounter), 2)
        # print stuff
        if randomEnvironment == True:
            print("\nThe agent was tested against a RANDOM environment with ", nMoves, "moves.")
        else:
            print("\nThe agent was tested against an AI environment with ", nMoves, "moves.")
        print("\nThe agent won ", winCounter, " times.")
        print("\nThe agent lost ", loseCounter, " times.")
        print("\nThe win frequency is ", winFrequency, "%.")
        # restore the old epsilon values
        self.epsilon = epsilonAgent
        environment.epsilon = epsilonEnvironment
        return winFrequency


    def train(self, environment, nTurns = 1000, greedyEnvironment = True, useLastExperience = True):
    	# make environment act greedly
        if greedyEnvironment == True:
    		# save epsilon environment
            epsilonEnvironment = copy.deepcopy(environment.epsilon)
            environment.epsilon = 0
        # initialize variable that controls while loop
        isAgentStronger = False
        # while the agent is weaker we keep training it
        while isAgentStronger == False:
        	# first we reset the memory
            self.reset_memory()
        	# and we create a new memory
            self.fill_memory(environment)
        	# initialize the board
            board = empty_board(self.NN.nRows, self.NN.nColumns)
            board.reset(self, environment)
            for turns in range(nTurns):
            	# we play one turn and we collect the experience (S,a,r,S_prime)
                experience = self.S_a_r_S_prime(board, environment)
                # update the memory
                self.update_memory(experience)
                # get a batch from memory
                batch = self.get_batch()
                # optionally, we can force the last experience to
                # be added in the batch
                if useLastExperience == True:
                    batch.append(experience)
                # use it for training
                self.NN.train_NN(batch)
            # let's save the trained model
            self.NN.save()
            # if agent can beat the environment, exit the loop!
            if self.test(environment) == 100:
                isAgentStronger = True
        # restore the old epsilon of environment
        environment.epsilon = epsilonEnvironment



