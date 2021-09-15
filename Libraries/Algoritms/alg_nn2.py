from os import stat
from pickle import TRUE
from Libraries.Structures.logger import LoggerInstance
from Libraries.Structures.settings import PARAMS
from random import uniform, randint
from math   import sqrt
from copy   import deepcopy
from Libraries.consts import DATE_TIME, ROW_MULTIPLER

from Libraries.vector import Vector

from Libraries.Structures.backupCreator import Backup

from keras.models import Sequential, save_model, load_model
from keras.layers import Dense
from collections import deque
import numpy as np
import random

class NeuralNetwork2:
    IS_LEARNABLE = True
    LEARNING_DELAY = 5
    delay = 0
    dateTime = ""

    NAME = ""

    def constuct_name(self):
        self.NAME = "2NeuralNetwork"
        self.NAME += str(len(PARAMS.HEURYSTIC)) + "_"
        self.NAME += str(PARAMS.MAX_POINTS) + "_"
        
        for i in PARAMS.NET_CONFIGURATION:
            self.NAME += str(i) + "_"
        for i in PARAMS.NET_OPTIMIZERS:
            self.NAME += i[0] + "+"
        self.NAME += PARAMS.OPTIMIZER + "_"
        self.NAME += PARAMS.LOSS +"_"
        self.NAME += str(PARAMS.BACH_SIZE) + "_"
        self.NAME += str(PARAMS.EPOCH) 


    def __init__(self, replay_start_size=None):
        self.constuct_name()

        self.n_neurons      = PARAMS.NET_CONFIGURATION
        self.activations    = PARAMS.NET_OPTIMIZERS
        self.loss           = PARAMS.LOSS
        self.optimizer      = PARAMS.OPTIMIZER

        print(PARAMS.NET_CONFIGURATION)

        assert len(self.activations) == len(self.n_neurons) + 1

        if Backup.load_neural_network(self) == False:
            self.memory    = deque(maxlen=PARAMS.MAX_POINTS)
            self.model     = self._build_model()
            self.discount  = 0.97
            self.epsilon   = 1
            self.dateTime = DATE_TIME

        self.file_save_name  = self.NAME + "_netChange"
        LoggerInstance.register_log( self.file_save_name, self.dateTime, "nn", continueSyle=(DATE_TIME!=self.dateTime))
        

        self.epsilon_min    = 0
        self.epsilon_decay  = 0.02

        if not replay_start_size: replay_start_size = PARAMS.MAX_POINTS/2
        self.replay_start_size = replay_start_size


    def _build_model(self):
        model = Sequential()
        model.add(Dense(self.n_neurons[0], 
                        input_dim=231, 
                        activation=self.activations[0]))

        for i in range(1, len(self.n_neurons)):
            model.add(Dense(self.n_neurons[i], activation=self.activations[i]))

        model.add(Dense(1, activation=self.activations[-1]))
        model.compile(loss=self.loss, optimizer=self.optimizer)
        return model

    def add_to_memory(self, current_state, next_state, reward, done):
        if len(current_state) != 231: 
            print("Can't add to memory : Invaid len " + str(len(current_state)))
            return


   #     if len(self.memory) == self.BUFFOR_SIZE:
  #          removable = self.memory[0]
 #           if self.epsilon > 0: self.memory.append(removable)
#
        self.memory.append((current_state, next_state, reward, done))

    def random_value(self):
        return random.random()

    def predict_value(self, state):
        return self.model.predict(state)[0]

    def act(self, state):
        state = np.reshape(state, [1, self.state_size])
        if random.random() <= self.epsilon:
            return self.random_value()
        else:
            return self.predict_value(state)

    def best_state(self, states):
        max_value  = None
        best_state = None
        best_key   = None

        if random.random() <= self.epsilon:
            return random.choice(list(states))
        else:
            for state_key in states.keys():
                state = states[state_key]
                value = self.predict_value(np.reshape(state, [1, 231]))
                if not max_value or value > max_value:
                    max_value  = value
                    best_state = state
                    best_key   = state_key

        return best_key

    Leartning_started = False

    def train(self):
        n = len(self.memory)
    
      #  print( n, self.delay )

        if self.Leartning_started == False:
            print("Buffor is full in " + str( len(self.memory)/PARAMS.MAX_POINTS) + "%")

        if n >= self.replay_start_size and n >= PARAMS.BACH_SIZE:
            self.delay += 1
            if self.delay < self.LEARNING_DELAY: return
            self.delay = 0

            self.Leartning_started = True

        #    print(len(self.memory))
            batch = random.sample(self.memory, PARAMS.BACH_SIZE)

            # Get the expected score for the next states, in batch (better performance)
            next_states = np.array([x[1] for x in batch])

           # print( "NextStates " + str(next_states) )

            new_qs = [x[0] for x in self.model.predict(next_states)]

           # print( "NextQS " + str(next_qs) )

            x = [x[0] for x in batch]
            y = [x[2] + self.discount * qs if not x[3] else 0 for x, qs in zip(batch, new_qs)]

            # Build xy structure to fit the model in batch (better performance)
            #for i, (state, next_state, reward, done) in enumerate(batch):

            #    if(len(state) != 231) : 
           #         print( "Invalid input " + str(len(state)))
            #        continue 

                #print(len(state))

            #    if not done:
                    # Partial Q formula
            #        new_q = reward + self.discount * new_qs[i]
           #     else:
           #         new_q = reward

            #    x.append(state)
            #    y.append(new_q)

          #  print( "X" + str(x) )
          #  print( "Y" + str(y) )
#
            # Fit the model to the given values
            hisory = self.model.fit(np.array(x), np.array(y), batch_size=PARAMS.BACH_SIZE, epochs=PARAMS.EPOCH, verbose=0)
            
            print(self.get_last_for(str(hisory.epoch)), self.get_last_for(str(hisory.history)))
          #  print( "FIT CALLED")

            Backup.save_neural_network(self)
            self.memory = deque(maxlen=PARAMS.MAX_POINTS, iterable=self.memory)

            # Update the exploration variable
            if self.epsilon > self.epsilon_min:
                self.epsilon -= self.epsilon_decay
               # self.BUFFOR_SIZE = 1028 + int( (1.0 - self.epsilon)/self.epsilon_decay ) * 5
               # self.memory = deque(maxlen=PARAMS.MAX_POINTS, iterable=self.memory)
               # self.
        else: self.Leartning_started = False

    def get_last_for(self, strings):
        strings.replace("[", "")
        strings.replace("]", "")
        obg = strings.split(",")
        return obg[len(obg)-1]
            

class NeuralNetworkFixed2: 
    IS_LEARNABLE = False
    model = None
    state_size = 0

    def __init__(self, modelName):
        self.model = load_model(modelName)
        self.state_size = len(PARAMS.HEURYSTIC)
        print("NeuralNetwork Loaded best for presenter app")

    def best_state(self, states):
        max_value  = None
        best_state = None
        best_key   = None

        for state_key in states.keys():
            state = states[state_key]
            value = self.predict_value(np.reshape(state, [1, 231]))
            if not max_value or value > max_value:
                max_value  = value
                best_state = state
                best_key   = state_key

        return best_key

    def predict_value(self, state):
        return self.model.predict(state)[0]

    def add_to_memory(self, current_state, next_state, reward, done): pass