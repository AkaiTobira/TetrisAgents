
from Libraries.consts import *
from Libraries.vector import Vector
from Libraries.Algoritms.particle import Particle
import json

class BackupCreator:
    particles = { 4 : [], 5 :[], 6 :[] }
    evolution = { 4 : [], 5 :[], 6 :[], "H4" : {}, "H5" : {}, "H6" : {} }

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

        print('Backups/Evo' + str(numberOfDimenstion) + ": Backup Loaded")
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

    def load_pso(self, numberOfDimenstion, sizeOfPopulation):
        json_converted = None
        with open('Backups/PSO' + str(numberOfDimenstion) + '.json', 'r') as json_file:
            json_converted = json.loads(json_file.read())

        if sizeOfPopulation != json_converted["particles_number"]:
            print(  'Backups/PSO' + str(numberOfDimenstion) + ": Backup is different, couldn't read from file")
            return False, [], 0, "", 0, None, 0

        population = []
        for i in range( sizeOfPopulation ):
            part = Particle( nmberOfDimension=numberOfDimenstion, curr_score=json_converted["particles"][i]["curr_score"])
            part.dir_v.v    = json_converted["particles"][i]["dir_v"]
            part.pos_v.v    = json_converted["particles"][i]["pos_v"]
            part.best_pos.v = json_converted["particles"][i]["best_pos"]
            part.curr_score = json_converted["particles"][i]["curr_score"]
            part.best_score = json_converted["particles"][i]["best_score"] 
            population.append( part )

        print('Backups/PSO' + str(numberOfDimenstion) + ": Backup Loaded")
        bestVector = Vector(numberOfDimenstion)
        bestVector.v = json_converted["best_particle_pos"]
        return True, population, json_converted["iteration"], json_converted["date_time"], json_converted["current_index"], bestVector, json_converted["best_score"]


    def save_pso(self, particles, currentParticleIndex, bestParticlePosition, bestScore, iteration, dateTime, numberOfDimenstions ):
        while len(self.particles[numberOfDimenstions]) != len(particles) :
            self.particles[numberOfDimenstions].append({
                "dir_v" : particles[len(self.particles[numberOfDimenstions]) - 1].dir_v.v,
                "pos_v" : particles[len(self.particles[numberOfDimenstions]) - 1].pos_v.v,
                "best_pos" : particles[len(self.particles[numberOfDimenstions]) -1].best_pos.v,
                "best_score" : particles[len(self.particles[numberOfDimenstions]) -1].best_score,
                "curr_score" : particles[len(self.particles[numberOfDimenstions]) -1].curr_score
            })
        
        self.particles[ numberOfDimenstions ][ currentParticleIndex ] = {
            "dir_v"      : particles[currentParticleIndex].dir_v.v,
            "pos_v"      : particles[currentParticleIndex].pos_v.v,
            "best_pos"   : particles[currentParticleIndex].best_pos.v,
            "best_score" : particles[currentParticleIndex].best_score,
            "curr_score" : particles[currentParticleIndex].curr_score
        }

        backup = {
            "date_time"         : dateTime,
            "iteration"         : iteration,
            "current_index"     : currentParticleIndex,
            "best_particle_pos" : bestParticlePosition.v,
            "best_score"        : bestScore,
            "particles_number"  : len(particles),
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME,
            "particles"        : self.particles[ numberOfDimenstions ]
        }

        with open('Backups/PSO' + str(numberOfDimenstions) + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

Backup = BackupCreator()