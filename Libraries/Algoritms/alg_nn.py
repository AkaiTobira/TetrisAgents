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

class NeuralNetwork:
    LEARNING_DELAY = 5
    BUFFOR_SIZE    = 1028
    delay = 0
    spawnerType = 0
    dateTime = ""

    def __init__(self, state_size, replay_start_size=None, spawnerType = 0):
        self.n_neurons      = [32, 32, 32]
        self.activations    = ['relu', 'relu', 'relu', 'linear']
        self.loss           = 'mse'
        self.optimizer      = 'adam'

        assert len(self.activations) == len(self.n_neurons) + 1

        self.state_size     = state_size
        self.spawnerType = spawnerType
        can_continue, model, memory, discount, epsilon, dateTime = Backup.load_neural_network(state_size, spawnerType)

        if can_continue:
            self.model    = model
            self.memory   = deque(memory, maxlen=self.BUFFOR_SIZE)
            self.discount = discount
            self.epsilon  = epsilon
            self.dateTime = dateTime

        #    print(self.memory[0])
        else:
            self.memory    = deque(maxlen=self.BUFFOR_SIZE)
            self.model     = self._build_model()
            self.discount  = 0.95
            self.epsilon   = 1
            self.dateTime = DATE_TIME

        self.epsilon_min    = 0
        self.epsilon_decay  = 0.002

        if not replay_start_size: replay_start_size = self.BUFFOR_SIZE/2
        self.replay_start_size = replay_start_size


    def _build_model(self):
        model = Sequential()
        model.add(Dense(self.n_neurons[0], 
                        input_dim=self.state_size, 
                        activation=self.activations[0]))

        for i in range(1, len(self.n_neurons)):
            model.add(Dense(self.n_neurons[i], activation=self.activations[i]))

        model.add(Dense(1, activation=self.activations[-1]))
        model.compile(loss=self.loss, optimizer=self.optimizer)
        return model

    def add_to_memory(self, current_state, next_state, reward, done):
        if len(current_state) != self.state_size: return

        if done == False:
            can_add = True
            if reward >= ROW_MULTIPLER : pass
            elif current_state[2] > next_state[2] : pass
            else : can_add = False

            if not can_add: return

        if len(self.memory) == self.BUFFOR_SIZE:
            removable = self.memory[0]
            if self.epsilon > 0: self.memory.append(removable)

        self.memory.append((current_state, next_state, reward if not done else -1000, done))
      #  
       # print((current_state, next_state, reward, done))

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
                value = self.predict_value(np.reshape(state, [1, self.state_size]))
                if not max_value or value > max_value:
                    max_value  = value
                    best_state = state
                    best_key   = state_key

        return best_key


    def train(self, batch_size=256, epochs=30):
        n = len(self.memory)
    
      #  print( n, self.delay )

        if n >= self.replay_start_size and n >= batch_size:
            self.delay += 1
            if self.delay < self.LEARNING_DELAY: return
            self.delay = 0
        #    print(len(self.memory))
            batch = random.sample(self.memory, batch_size)

            # Get the expected score for the next states, in batch (better performance)
            next_states = np.array([x[1] for x in batch])

           # print( "NextStates " + str(next_states) )

            next_qs = [x[0] for x in self.model.predict(next_states)]

           # print( "NextQS " + str(next_qs) )

            x = []
            y = []

            # Build xy structure to fit the model in batch (better performance)
            for i, (state, _, reward, done) in enumerate(batch):
                if not done:
                    # Partial Q formula
                    new_q = reward + self.discount * next_qs[i]
                else:
                    new_q = reward

                x.append(state)
                y.append(new_q)

          #  print( "X" + str(x) )
          #  print( "Y" + str(y) )
#
            # Fit the model to the given values
            self.model.fit(np.array(x), np.array(y), batch_size=batch_size, epochs=epochs, verbose=0)

          #  print( "FIT CALLED")

            Backup.save_neural_network(self)

            # Update the exploration variable
            if self.epsilon > self.epsilon_min:
                self.epsilon -= self.epsilon_decay
                self.BUFFOR_SIZE = 1028 + int( (1.0 - self.epsilon)/self.epsilon_decay ) * 5
                self.memory = deque(maxlen=self.BUFFOR_SIZE, iterable=self.memory)
               # self.

class NeuralNetworkFixed: 
    model = None
    state_size = 0

    def __init__(self, modelName, state_size):
        self.model = load_model(modelName)
        self.state_size = state_size
        print("NeuralNetwork Loaded best for presenter app")

    def best_state(self, states):
        max_value  = None
        best_state = None
        best_key   = None

        for state_key in states.keys():
            state = states[state_key]
            value = self.predict_value(np.reshape(state, [1, self.state_size]))
            if not max_value or value > max_value:
                max_value  = value
                best_state = state
                best_key   = state_key

        return best_key

    def predict_value(self, state):
        return self.model.predict(state)[0]

    def add_to_memory(self, current_state, next_state, reward, done): pass