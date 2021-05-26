#--------------------------------------------
# THINGS TO DO
#
# > clean the test vs random
# > write an interface to play against the AI

from board import *
from AI import *
from NN import *

import numpy as np 
import matplotlib.pyplot as plt

def main():
    board = empty_board(6,7)
    neuralNet1 = NN(name="exp1", nEpochs = 1, nRows=6, nColumns=7, learningRate = 0.003, freezeSteps = 10)
    neuralNet2 = NN(name="exp2", nEpochs=1, nRows=6, nColumns=7, learningRate = 0.003, freezeSteps = 10)

    ai1= AI(1, NN = neuralNet1, epsilon = 0.15, memorySize = 50, batchSize = 6)
    ai2 = AI(2,  NN = neuralNet2, epsilon = 0.15, memorySize = 50, batchSize = 6)
    ai1.fill_memory(ai2)
    ai2.fill_memory(ai1)
    #print(agent.memory)
    #environment.create_memory(agent)
    #agent.action(board)
    #print(board.playerToPlay)
    #environment.action(board)
    #print(board.playerToPlay)
    beatRandom = False
    counter = 0

    winFreq1_vec = []
    winFreq2_vec = []
    while beatRandom == False:
        ai1.train(ai2, nTurns = 100)
        winFreq1 = ai1.test(ai2, randomEnvironment=True)
        if winFreq1 > 95:
            beatRandom = True
        ai2.train(ai1,nTurns = 100)
        winFreq2 = ai2.test(ai1, randomEnvironment=True)
        if winFreq2 > 95:
            beatRandom = True
        # PLOT STUFF
        counter += 1
        winFreq1_vec.append(winFreq1)
        winFreq2_vec.append(winFreq2)
        plt.plot(range(counter), winFreq1_vec, label="Win frequency of ai1 vs random", color='blue')
        plt.plot(range(counter), winFreq2_vec, label="Win frequency of ai2 vs random", color='red')
        plt.pause(0.05)
    plt.show()

main()
