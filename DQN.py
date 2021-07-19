# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:38:00 2020

@author: iainr
"""
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import numpy as np
from collections import deque
import time
import random

REPLAY_MEMORY_SIZE = 50000
MIN_REPLAY_MEMORY_SIZE = 1000
MODEL_NAME = "256x2"
MINIBATCH_SIZE = 64 

class DQNAgent:
    def __init__(self):
        # main model (gets trained every step)
        self.model = self.createModel()
        
        # target model (this is what we .predict against every step)
        self.targetModel = self.createModel()
        self.targetModel.set_weights(self.model.get_weights())
        
        self.replayMemory = deque(maxle=REPLAY_MEMORY_SIZE)
        
        self.tensorboard = ModifiedTensorBoard(log_dir=f"logs/{MODEL_NAME}-{int(time.time())}")
        
        self.targetUpdateCounter = 0
              
               
    def createModel(self):
        model = Sequential()
        model.add(Conv2D(256, (3,3), input_shape=env.OBSERVATION_SPACE_VALUES))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(0.2))
     
        model.add(Conv2D(256, (3,3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(0.2))
        
        model.add(Flatten())
        model.add(Dense(64))
        
        model.add(Dense(env.ACTION_SPACE_SIZE, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=["accuracy"])
        
        return model
    
    
    def updateReplayMemory(self, transition):
        self.replayMemory.append(transition)
        
    
    def getQs(self, terminalState, step):
        
        return self.modelPrecit(np.array(state).reshape(-1, *state.shape)/255)[0]
    
    
    def train(self, terminalState, step):
        if len(self.replayMemory) < MIN_REPLAY_MEMORY_SIZE:
            return
        
        minibatch = random.sample(self.replayMemory, MINIBATCH_SIZE)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
# Own Tensorboard class
class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.FileWriter(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

        