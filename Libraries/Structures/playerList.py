import pygame

from Libraries.Agents.agent_human      import HumanPlayer
from Libraries.Agents.agent_grad       import GradAi
from Libraries.Agents.agent_evolution  import EvolutionAi
from Libraries.Agents.agent_nnetwork   import NeuralEvolutionAi
from Libraries.Agents.agent_pso        import PSOAi
from Libraries.Agents.agent_rlearning  import ReinforcmentLearning
from Libraries.Agents.agent_rnetwork   import ReinforcmentNetwork
from Libraries.Structures.best_saver   import instance

class PlymodeController:
    learning_modes = {}
    last_pressed_player_key = pygame.K_1
    switching_enabled = True

    def __init__( self, switch_enabled = True ):
        self.switching_enabled = switch_enabled
        self.learning_modes = {
            pygame.K_1 : HumanPlayer(),
            pygame.K_2 : EvolutionAi(),
            pygame.K_3 : PSOAi(),
            pygame.K_4 : ReinforcmentNetwork(),
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


class PresenterBotsController:
    bots = []

    def __init__( self ): 

        self.bots = [    
                    PresenterBotUnit(EvolutionAi( instance.getLastBest("Evolution4")) ),
                    PresenterBotUnit(EvolutionAi( instance.getLastBest("Evolution4") )),
                    PresenterBotUnit(EvolutionAi( instance.getLastBest("Evolution4") )),
                    PresenterBotUnit(EvolutionAi( instance.getLastBest("Evolution4") )),
                    PresenterBotUnit(EvolutionAi( instance.getLastBest("Evolution4") )),
         ]

    def getBotUnit( self, index ): 
        return self.bots[index]


class PresenterBotUnit:
    playerUnit = None

    def __init__( self, bot ): 
        self.playerUnit = bot

    def get_player(self, playerIndex): return self.playerUnit

    def get_active_player(self): return self.playerUnit

    def game_over_feedback(self, score, number_of_tetrominos): pass

    def process(self, event): pass
    
    def is_AI_Player(self): return True


