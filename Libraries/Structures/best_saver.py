


import json
from os import close
from Libraries.consts  import ROW_MULTIPLER

class BestUnitSaver:
    controll_file  = None
    json_converted = None 

    def __init__(self) -> None:
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())
        json_file.close()

    def saveNeuralNetwork(self, name, score, model):
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())

        if (not name in self.json_converted) or score > self.json_converted[name]["score"]["combined"] :
            print("Found better in : " + name + " with score " + str(score))
            self.json_converted[name] = { 
                "body"  : "Best" + name, 
                "score" : { "combined"     : score,
                            "cleared_rows" : int(score/ROW_MULTIPLER), 
                            "cleared_tetrimino" : int(score%ROW_MULTIPLER)}
            }
            model.save("Best" + name)
            self.saveDump()

    def saveScore(self, name, value, score):
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())


        if( (not name in self.json_converted) or score > self.json_converted[name]["score"]["combined"] ):
            print("Found better in : " + name + " with score " + str(score))

            self.json_converted[name] = { "body"   : list(value), 
                                        "score" : { "combined"     : score,
                                                    "cleared_rows" : int(score/ROW_MULTIPLER), 
                                                    "cleared_tetrimino" : int(score%ROW_MULTIPLER)}
            }

            self.saveDump()

    def getLastBest(self, name):
        return self.json_converted[name]["body"]

    def printFile(self):
        print( self.json_converted )

    def saveDump(self):
        with open('logs/bestBackup.json', 'w') as outfile:
            json.dump(self.json_converted, outfile, indent=4)
        

BestUnitsBackupSaver = BestUnitSaver()
