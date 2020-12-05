
from Libraries.consts import *
from Libraries.vector import Vector
import json

class BackupCreator:
    def __init__(self): pass

    def load_evolution(self, numberOfDimenstion, numberInPopulation, number_of_games):
        json_converted = None
        with open('Backups/Evo' + str(numberOfDimenstion) + '.json', 'r') as json_file:
            json_converted = json.loads(json_file.read())

        if numberInPopulation != json_converted["population_size"] or number_of_games != json_converted["number_of_games"]:
            print(  'Backups/Evo' + str(numberOfDimenstion) + ": Backup is different, couldn't read from file")
            return False, [], 0, ""

        if numberInPopulation != len(json_converted["population"]):
            print(  'Backups/Evo' + str(numberOfDimenstion) + ": File data corrupted, couldn't read from file")
            return False, [], 0, ""

        population = []
        for i in range( numberInPopulation ):
            vec = Vector(numberOfDimenstion)
            vec.v =  json_converted["population"][i]["values"]
            population.append( [ vec, json_converted["population"][i]["score"]] )

        print("Backup Loaded")
        return True, population, json_converted["generation"], json_converted["date_time"]

    def save_evolution(self, population, generation, dateTime, mutationrate, number_of_games, numberOfDimesions):
        backup = {
            "generation"      : generation,
            "date_time"       : dateTime,
            "number_of_games" : number_of_games,
            "population_size" : len(population),
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME,
            "mutation_rate"   : mutationrate,
            "population"      : []
        }

        for i in range( len(population) ):
            backup["population"].append( {
                "score"  : population[i][1],
                "values" : population[i][0].v
            })

        with open('Backups/Evo' + str(numberOfDimesions) + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)


Backup = BackupCreator()