# Class NN (neural network)
#
# METODS:
#
# evaluate
# create_train_data
# save

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, losses
import tensorflow.keras.backend as kb
import copy
import matplotlib.pyplot as plt

class NN:
    def __init__(self, name, nRows, nColumns, nEpochs=3, learningRate=0.001, gamma = 0.95, freezeSteps = 20):
        self.name = name
        self.nRows = nRows
        self.nColumns = nColumns
        self.nEpochs = nEpochs
        self.learningRate = learningRate
        self.gamma = gamma
        # create the actual neural network:
        try:
            # check whether there is already a NN with that name
            self.neuralNetwork = tf.keras.models.load_model('NN_parameters/NN_' + self.name)
        except:
            # otherwise create a new NN 
            self.neuralNetwork = tf.keras.Sequential([
                layers.Conv2D(40, (4, 4), activation='sigmoid', padding = 'same', input_shape=(nRows, nColumns, 1)),
                layers.Dropout(0.1),
                layers.Flatten(),
                layers.Dense(256, activation='sigmoid'),  # This can be changed later
                layers.Dropout(0.1),
                layers.Dense(nColumns, activation='sigmoid')  # The number of actions is equal to the number of columns
            ])
        self.neuralNetwork.compile(optimizer='SGD',
            loss='mse',
            metrics=[tf.keras.metrics.MeanSquaredError()])
        # save the model
        self.neuralNetwork.save('NN_parameters/NN_' + self.name)
        # create a frozen copy of the NN 
        # this a copy of the keras model self.neuralNetwork but its weights will be
        # updated every self.freezeSteps of training 
        # (this trick should help stabilizing the learning process) 
        self.frozen = tf.keras.models.load_model('NN_parameters/NN_' + self.name)
        self.frozen.save('NN_parameters/NN_' + self.name + '_frozen')
        # set a counter for the freezing steps
        self.freezeCounter = 0
        self.freezeSteps = freezeSteps


    def updateFrozen(self):
    	# increase the counter
        self.freezeCounter = (self.freezeCounter + 1) % self.freezeSteps
        if self.freezeCounter == 0:
        	# if the counter is 0 % freeze steps, we copy the weights from the neural network
            self.frozen.set_weights(self.neuralNetwork.get_weights())


    def frozenEvaluate(self, matrix):
        # This method makes the frozen NN evaluate a matrix.
        # it should be used only to compute the target 
        currentState = matrix
        (nRows, nColumns) = np.shape(currentState)
        currentState = currentState.reshape(1, nRows, nColumns, 1)
        return np.array(self.frozen(currentState)[0]) 


    def evaluate(self, matrix):
        # This method makes the NN evaluate a matrix. 
        currentState = matrix
        (nRows, nColumns) = np.shape(currentState)
        currentState = currentState.reshape(1, nRows, nColumns, 1)
        return np.array(self.neuralNetwork(currentState)[0])


    def create_train_data(self, batch):
    	# This creates the training data (train, target) from a batch of memory
    	# !!! NN_frozen is in instance of the NN class and 
        xTrain = []
        target = []
        for exp in range(len(batch)):
            action = batch[exp][1]
            S = copy.deepcopy(batch[exp][0])
            # if reward is not zero then we end up in a terminal state
            if batch[exp][2] == 0:
                # Note that for non-terminal states we use the frozen NN to
                # create the target 
                actualTarget = self.gamma * np.max(self.frozenEvaluate(batch[exp][3]))
            else:
                actualTarget = batch[exp][2]
            vector = copy.deepcopy(self.evaluate(S))
            vector[action] = actualTarget
            target.append(vector)
            xTrain.append(S)
        target = np.array(target)
        xTrain = np.array(xTrain)
        xTrain = xTrain.reshape(len(batch), self.nRows, self.nColumns, 1)
        return xTrain, target


    def train_NN(self, batch):
    	# This method train a NN with a given a batch experience
        xTrain, target = self.create_train_data(batch)
    	# Note that (xTrain, target) could be the output of the metod create_train_data
    	# of another NN.
        history = self.neuralNetwork.fit(xTrain, target, batch_size=len(batch), epochs = self.nEpochs)
        # print history
        # update frozen NN
        self.updateFrozen()
        return history.history['loss'][-1]


    def save(self):
        self.neuralNetwork.save('NN_parameters/NN_' + self.name)
