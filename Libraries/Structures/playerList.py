import pygame

from Libraries.Agents.agent_human      import HumanPlayer
from Libraries.Agents.agent_grad       import GradAi
from Libraries.Agents.agent_evolution  import EvolutionAi
from Libraries.Agents.agent_nnetwork   import NeuralEvolutionAi
from Libraries.Agents.agent_pso        import PSOAi
from Libraries.Agents.agent_rlearning  import ReinforcmentLearning
from Libraries.Agents.agent_rnetwork   import ReinforcmentNetwork

class PlymodeController:
    learning_modes = {}
    last_pressed_player_key = pygame.K_1
    switching_enabled = True

    def __init__( self, switch_enabled = True ):
        self.switching_enabled = switch_enabled
        self.learning_modes = {
            pygame.K_1 : HumanPlayer(),
            pygame.K_2 : EvolutionAi(),
        }

    def get_player(self, playerIndex):
        return self.learning_modes[self.learning_modes.keys[playerIndex]]

    def get_active_player(self):
        return self.learning_modes[self.last_pressed_player_key]

    def game_over_feedback(self, score, number_of_tetrominos):
        self.learning_modes[self.last_pressed_player_key].game_over_feedback(score, number_of_tetrominos)

    def process(self, event):
        if not self.switching_enabled : return
        if event.type == pygame.KEYUP:
            if event.key in self.learning_modes.keys():
                toList = list(self.learning_modes.keys())
                index = toList.index(event.key)
                self.last_pressed_player_key = toList[index]

    def is_AI_Player(self):
        return self.last_pressed_player_key != pygame.K_1




#players       = [ None      ]# EvolutionAi(), GradAi(),   PSOAi(),    ReinforcmentNetwork()] #NeuralEvolutionAi(), ReinforcmentLearning()]#, PredifinedLearning() ]
#players_keys  = [ ]#, pygame.K_2,    pygame.K_3, pygame.K_4, pygame.K_5           ] #pygame.K_5,          pygame.K_6,           ]#  pygame.K_7]

