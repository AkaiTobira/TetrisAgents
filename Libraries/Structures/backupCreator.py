
from Libraries.consts import *
from Libraries.vector import Vector
from Libraries.Algoritms.particle import Particle
from keras.models     import Sequential, save_model, load_model

import json

class BackupCreator:
    particles = { 4 : [], 5 :[], 6 :[] }

    def __init__(self): pass

    def save_neural_network(self, neuralNetwork):
        backup = {
            "input_size" : neuralNetwork.state_size,
            "date_time"  : neuralNetwork.dateTime,
            "model_path" : "logs/nn/" + neuralNetwork.dateTime,
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME_NN,
            "epsilon"    : neuralNetwork.epsilon,
            "discount"   : neuralNetwork.discount,
            "memory"     : list(neuralNetwork.memory)
        }

        neuralNetwork.model.save(backup["model_path"])

        with open('Backups/NN.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

    def load_neural_network(self, inputSize):
        json_converted = None
        with open('Backups/NN.json', "r") as json_file:
            json_converted = json.loads(json_file.read())

        if inputSize != json_converted["input_size"] or MAX_NUMBER_PER_GAME_NN != json_converted["number_of_tetrominos_per_game"]:
            print( "Backups/NN : Backup is different, couldn't read from file")
            return False, None, [], 0, 0, ""

        model  = load_model( json_converted["model_path"])
        memory = json_converted["memory"]
        return True, model, memory, json_converted["discount"], json_converted["epsilon"], json_converted["date_time"]


    def load_evolution(self, numberOfDimenstion, numberInPopulation, number_of_games):
        json_converted = None
        with open('Backups/Evo' + str(numberOfDimenstion) + '.json', 'r') as json_file:
            json_converted = json.loads(json_file.read())

        if number_of_games != json_converted["number_of_games"] or MAX_NUMBER_PER_GAME_EVO != json_converted["number_of_tetrominos_per_game"] :
            print(  'Backups/Evo' + str(numberOfDimenstion) + ": Backup is different, couldn't read from file")
            return False, [], [], 0, ""

        population = []
        for i in range( len( json_converted["population"]) ):
            vec = Vector(numberOfDimenstion)
            vec.v =  json_converted["population"][i]["values"]
            population.append( [ vec, json_converted["population"][i]["score"]] )

        to_check = []
        for i in range( len( json_converted["to_check"]) ):
            vec = Vector(numberOfDimenstion)
            vec.v =  json_converted["to_check"][i]["values"]
            to_check.append( [ i, vec, 0] )

        print('Backups/Evo' + str(numberOfDimenstion) + ": Backup Loaded")
        return True, population, to_check, json_converted["generation"], json_converted["date_time"]

    def save_evolution(self, evolutionAlgoritm):
        backup = {
            "generation"      : evolutionAlgoritm.generation,
            "date_time"       : evolutionAlgoritm.dateTime,
            "number_of_games" : evolutionAlgoritm.NUMBER_OF_PLAYED_GAMES,
            "population_size" : len(evolutionAlgoritm.population),
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME_EVO,
            "mutation_rate"   : evolutionAlgoritm.MUTATION_RATE,
            "population"      : [],
            "to_check"        : []
        }

        for i in range( len(evolutionAlgoritm.population) ):
            if i >= evolutionAlgoritm.POPULATION_SIZE + evolutionAlgoritm.NEW_POPULATION_SIZE: continue
            backup["population"].append( {
                "score"  : evolutionAlgoritm.population[i][1],
                "values" : evolutionAlgoritm.population[i][0].v
            })

        for i in range( len(evolutionAlgoritm.unchecked_population) ):
            if i >= evolutionAlgoritm.NEW_POPULATION_SIZE: continue
            backup["to_check"].append( {
                "values"  : evolutionAlgoritm.unchecked_population[i][1].v
            })

        print( len(backup["population"]), len(backup["to_check"]) )

        with open('Backups/Evo' + str(evolutionAlgoritm.EVOLUTION_VECTOR_DIMENSIONS) + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

    def load_pso(self, numberOfDimenstion, sizeOfPopulation):
        json_converted = None
        with open('Backups/PSO' + str(numberOfDimenstion) + '.json', 'r') as json_file:
            json_converted = json.loads(json_file.read())

        if sizeOfPopulation != json_converted["particles_number"] or MAX_NUMBER_PER_GAME_PSO != json_converted["number_of_tetrominos_per_game"]:
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
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME_PSO,
            "particles"        : self.particles[ numberOfDimenstions ]
        }

        with open('Backups/PSO' + str(numberOfDimenstions) + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

Backup = BackupCreator()