


import json
from os import close
from Libraries.consts  import ROW_MULTIPLER
from Libraries.Structures.settings import *

class BestUnitSaver:
    controll_file  = None
    json_converted = None 

    def __init__(self) -> None:
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())
        json_file.close()

    def saveNeuralNetwork(self, instance, score):
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())

        if (not instance.NAME in self.json_converted) or score > self.json_converted[instance.NAME]["score"]["combined"] :
            print("Found better in : " + instance.NAME + " with score " + str(score))
            self.json_converted[instance.NAME] = { 
                "body"  : "Backups/Networks/B" + instance.NAME, 
                "score" : { "combined"     : score,
                            "cleared_rows" : int(score/ROW_MULTIPLER), 
                            "cleared_tetrimino" : int(score%ROW_MULTIPLER)},
                "heurystics" : list(PARAMS.HEURYSTIC)
            }
            instance.model.save("Backups/Networks/B" + instance.NAME)
            self.saveDump()

    def saveScore(self, name, value, score, generation = 0):
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())


        if( (not name in self.json_converted) or score > self.json_converted[name]["score"]["combined"] ):
            print("Found better in : " + name + " with score " + str(score))

            self.json_converted[name] = { "body"   : list(value), 
                                        "heurystics" : list(PARAMS.HEURYSTIC),
                                        "score" : { "combined"     : score,
                                                    "generation"   : generation,
                                                    "cleared_rows" : int(score/ROW_MULTIPLER), 
                                                    "cleared_tetrimino" : int(score%ROW_MULTIPLER)}
            }

            self.saveDump()

    def hasScoreFor(self, name):
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())
        return name in self.json_converted.keys()

    def getLastBest(self, name):
        PARAMS.HEURYSTIC = self.json_converted[name]["heurystics"]
        PARAMS.HEURYSTIC_AMOUNT = len(PARAMS.HEURYSTIC)
        return self.json_converted[name]["body"]

    def getLastBestScore(self, name):
        if name in self.json_converted.keys():
            PARAMS.HEURYSTIC = self.json_converted[name]["heurystics"]
            PARAMS.HEURYSTIC_AMOUNT = len(PARAMS.HEURYSTIC)
            return self.json_converted[name]["score"]["combined"]
        return 0

    def printFile(self):
        print( self.json_converted )

    def saveDump(self):
        with open('logs/bestBackup.json', 'w') as outfile:
            json.dump(self.json_converted, outfile, indent=4)
        

BestUnitsBackupSaver = BestUnitSaver()
