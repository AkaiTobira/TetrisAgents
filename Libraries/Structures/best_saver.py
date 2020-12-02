


import json
from Libraries.consts  import ROW_MULTIPLER

# some JSON:
#x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:


# the result is a Python dictionary:
#print(y["age"]) 

#if

class BestUnitSaver:
    controll_file  = None
    json_converted = None 

    def __init__(self):
        #self.controll_file = open("logs/bestBackup.json", "r")
        with open('logs/bestBackup.json') as json_file:
            self.json_converted = json.loads(json_file.read())
        self.printFile()

    def saveScore(self, name, value, score):

        if( score > self.json_converted[name]["score"]["combined"] ):
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
        

instance = BestUnitSaver()
