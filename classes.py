# Classes

# Board class
class Board:
    def __init__(self, colorPlayer1 = 1, colorPlayer2 = -1, empty = 0):
        self.colorPlayer1 = colorPlayer2
        self.colorPlayer2 = colorPlayer2
        self.empty = empty

    def is_full(self):
        pass
        # TO WRITE !!!

    def is_winning(self, lastMove):
        pass
        # TO WRITE

    def print(self):
        # TO WRITE
        pass


# Class AI (a possible extra attribute could be "policy")
class AI:
    def __init__(self, whichPlayer, NN, epsilon):
        self.whichPlayer = whichPlayer
        self.NN = NN
        self.epsilon = epsilon

    def move(self, board):
        # TO WRITE
        pass



# Class NN (neural network)
class NN:
    def __init__(self, inputSize, nEpochs, learningRate):
        self.inputSize = inputSize
        self.nEpochs = nEpochs
        self.learningRate = learningRate

    def createTarget(self):
        # TO WRITE (NOTE! SOME OTHER ARGUMENTS (MEMORY/BATCH) ARE NEEDED!!)
        pass

# Class Memory
class Memory:
    def __init__(self, size, batchSize):
        self.size = size
        self.batchSize = batchSize

    def getBatch(self):
        # TO WRITE
        pass

    def update(self):
        # TO WRITE
        pass