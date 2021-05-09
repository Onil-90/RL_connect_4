# Class NN (neural network)
#
# METODS:
#
# evaluate
# create_target

class NN:
    def __init__(self, inputSize, nEpochs, learningRate, neuralNetwork=None):
        self.inputSize = inputSize
        self.nEpochs = nEpochs
        self.learningRate = learningRate
        self.neuralNetwork = neuralNetwork

    def evaluate(self, board):
    	# This method makes the NN evaluate the moves. 
    	# Note that board is assumed to be of the class Board
    	import numpy as np
        currentState = board.matrix
        (nRows, nColumns) = np.shape(currentState)
        currentState = currentState.reshape(1, nRows, nColumns, 1)
        return np.array(self.neuralNetwork(currentState)[0])


    def create_target(self):
        # TO WRITE (NOTE! SOME OTHER ARGUMENTS (MEMORY/BATCH) ARE NEEDED!!)
        pass
