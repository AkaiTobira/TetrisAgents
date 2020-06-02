from random import uniform, randint
from math   import sqrt
from copy   import deepcopy
from consts import DATE_TIME

from vector import Vector

from keras.models import Sequential, save_model, load_model
from keras.layers import Dense
from collections import deque
import numpy as np
import random


class NeuralNetwork:


    def __init__(self, state_size, replay_start_size=None):

        self.state_size     = state_size
        self.memory         = deque(maxlen=10000)
        self.discount       = 0.95
        self.epsilon        = 1
        self.epsilon_min    = 0
        self.epsilon_decay  = (1 - 0) / (500)
        self.n_neurons      = [32,32]
        self.activations    = ['relu', 'relu', 'linear']

        assert len(self.activations) == len(self.n_neurons) + 1

        self.loss           = 'mse'
        self.optimizer      = 'adam'
        if not replay_start_size:
            replay_start_size  = 5000
        self.replay_start_size = replay_start_size
        self.model             = self._build_model()

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
                value = self.predict_value(np.reshape(state, [1, self.state_size]))
                if not max_value or value > max_value:
                    max_value  = value
                    best_state = state
                    best_key   = state_key

        return best_key


    def train(self, batch_size=32, epochs=3):
        n = len(self.memory)
    
        print( n )

        if n >= self.replay_start_size and n >= batch_size:

            batch = random.sample(self.memory, batch_size)

            # Get the expected score for the next states, in batch (better performance)
            next_states = np.array([x[1] for x in batch])
            next_qs = [x[0] for x in self.model.predict(next_states)]

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

            # Fit the model to the given values
            self.model.fit(np.array(x), np.array(y), batch_size=batch_size, epochs=epochs, verbose=0)

            print( "FIT CALLED")

            # Update the exploration variable
            if self.epsilon > self.epsilon_min:
                self.epsilon -= self.epsilon_decay