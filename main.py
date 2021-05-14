from NN import *
from AI import *
from board import *


def main():
	board = empty_board(6,7)
    neuralNet1 = NN(name="exp1", nRows=6, nColumns=7)
    neuralNet2 = NN(name="exp2", nRows=6, nColumns=7)

    ai1= AI(1, NN = neuralNet1, epsilon = 0.2, memorySize = 10)
    ai2 = AI(2,  NN = neuralNet2, epsilon = 0.2, memorySize = 10)
    ai1.fill_memory(ai2)
    ai2.fill_memory(ai1)
    

    ai1.train(ai2, nTurns = 100)
    ai2.train(ai1,nTurns = 100)
    ai1.test(ai2, randomEnvironment=True)


if __name__ == '__main__':
    main()