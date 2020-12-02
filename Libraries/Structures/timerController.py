
from Libraries.Structures.playerList import PlymodeController
from Libraries.consts import *


class TimerController:
    playerList = None
    last_presed_key = AppKeys.SetTimerOne
    keys_to_react   = { AppKeys.SetTimerZero : 0.0, AppKeys.SetTimerInfinity : 10000, AppKeys.SetTimerOne : 1.0, AppKeys.SetTimerFastButSeen : 0.1 }

    def __init__(self, playerList ):
        self.playerList = playerList

    def process(self, event):
        if event.type == pygame.KEYUP:
            if event.key in self.keys_to_react.keys():
                toList = list(self.keys_to_react.keys())
                index = toList.index(event.key)
                self.last_presed_key = toList[index]
    

    def getTimeDelay(self):
        #if self.playerList.is_AI_Player():
        #    return 0.0
        return self.keys_to_react[self.last_presed_key]

    def reset(self):
        last_presed_key = AppKeys.SetTimerOne
