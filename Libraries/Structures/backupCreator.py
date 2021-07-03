
from Libraries.consts import *
from Libraries.vector import Vector
from Libraries.Algoritms.particle import Particle
from keras.models     import Sequential, save_model, load_model

import json

class BackupCreator:
    particles = { 4 : [], 5 :[], 6 :[],  7 :[], 10:[] }

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

        with open('Backups/NN'+ str(neuralNetwork.spawnerType) +'.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

    def load_neural_network(self, inputSize, spawnerType):
        json_converted = None

        try:
            with open('Backups/NN_' + str(spawnerType) +  '.json', "r") as json_file:
                json_converted = json.loads(json_file.read())
        except IOError:
            return False, [], [], 0, 0

        if inputSize != json_converted["input_size"] or MAX_NUMBER_PER_GAME_NN != json_converted["number_of_tetrominos_per_game"]:
            print( "Backups/NN_"  + str(spawnerType) + " : Backup is different, couldn't read from file")
            return False, None, [], 0, 0, ""

        model  = load_model( json_converted["model_path"])
        memory = json_converted["memory"]
        return True, model, memory, json_converted["discount"], json_converted["epsilon"], json_converted["date_time"]


    def load_evolution(self, numberOfDimenstion, numberInPopulation, number_of_games, spawnerType, learningTyep, m_rate):
        json_converted = None

        try:
            with open('Backups/Evo' + str(numberOfDimenstion) + "_G" + str(spawnerType) + "_D" + str(number_of_games) + "_T" + str(learningTyep) + "_MAX" + str(MAX_NUMBER_PER_GAME_EVO) + "_P" + str(numberInPopulation) + "_M" + str(m_rate) + '.json', 'r') as json_file:
                json_converted = json.loads(json_file.read())

            
        except IOError:
            #if(learningTyep == 1):
            #    try:
            #        with open('Backups/Evo' + str(numberOfDimenstion) + "_G" + str(spawnerType) + "_D" + str(number_of_games) + '_T1.json', 'r') as json_file:
            #            json_converted = json.loads(json_file.read())
            #    except IOError:
            #        return False, [], [], 0, 0
            #else: 
            return False, [], [], 0, 0

        if "restart" in json_converted.keys():
            if json_converted["restart"] == True: 
                print(  'Backups/Evo' + str(numberOfDimenstion) + "_" + str(spawnerType) + "_" + str(numberOfDimenstion)  + ": Backup reset")
                return False, [], [], 0, ""

        if MAX_NUMBER_PER_GAME_EVO != json_converted["number_of_tetrominos_per_game"] :
            print(  'Backups/Evo' + str(numberOfDimenstion) + "_" + str(spawnerType) + "_" + str(numberOfDimenstion)  + ": Backup is different, couldn't read from file")
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

        print('Backups/Evo' + str(numberOfDimenstion) + "_" + str(spawnerType) + ": Backup Loaded")
        return True, population, to_check, json_converted["generation"], json_converted["date_time"]

    def save_evolution(self, evolutionAlgoritm):
        backup = {
            "generation"      : evolutionAlgoritm.generation,
            "date_time"       : evolutionAlgoritm.dateTime,
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME_EVO,
            "left_to_process" : len(evolutionAlgoritm.unchecked_population),
            "number_of_games" : evolutionAlgoritm.NUMBER_OF_PLAYED_GAMES,
            "reset"           : False,
            "population_size" : len(evolutionAlgoritm.population),
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

       # print( len(backup["population"]), len(backup["to_check"]) )
        with open('Backups/Evo' + str(evolutionAlgoritm.EVOLUTION_VECTOR_DIMENSIONS) + "_G" + str(evolutionAlgoritm.spawnerType) + "_D" + str(evolutionAlgoritm.NUMBER_OF_PLAYED_GAMES)  +  "_T" + str(evolutionAlgoritm.TYPE) + "_MAX" + str(MAX_NUMBER_PER_GAME_EVO) + "_P" + str(evolutionAlgoritm.POPULATION_SIZE) + "_M" + str(evolutionAlgoritm.MUTATION_RATE)  + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

    def load_pso(self, numberOfDimenstion, sizeOfPopulation, spawnerType, c1, c2, w):
        fileName = 'Backups/PSO' + str(numberOfDimenstion)
        fileName += "_G" + str(spawnerType)
        fileName += "_P" + str(sizeOfPopulation)
        fileName += "_TMAX" + str(MAX_NUMBER_PER_GAME_PSO)
        fileName += "_C1-" + str(c1)
        fileName += "_C2-" + str(c2)
        fileName += "_W-"  + str(w)

        json_converted = None
        try:
            with open(fileName + '.json', 'r') as json_file:
                json_converted = json.loads(json_file.read())
        except IOError:
            return False, [], 0, "", 0, None, 0

        if sizeOfPopulation != json_converted["particles_number"] or MAX_NUMBER_PER_GAME_PSO != json_converted["number_of_tetrominos_per_game"]:
            print(  fileName + ": Backup is different, couldn't read from file")
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

        print(fileName+  ": Backup Loaded")
        bestVector = Vector(numberOfDimenstion)
        bestVector.v = json_converted["best_particle_pos"]
        return True, population, json_converted["iteration"], json_converted["date_time"], json_converted["current_index"], bestVector, json_converted["best_score"]


    def save_pso(self, particles, currentParticleIndex, bestParticlePosition, bestScore, iteration, dateTime, numberOfDimenstions, spawnerId, c1, c2, w ):
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
            "c1"                : c1,
            "c2"                : c2,
            "w"                 : w,
            "current_index"     : currentParticleIndex,
            "best_particle_pos" : bestParticlePosition.v,
            "best_score"        : bestScore,
            "particles_number"  : len(particles),
            "number_of_tetrominos_per_game" : MAX_NUMBER_PER_GAME_PSO,
            "particles"        : self.particles[ numberOfDimenstions ]
        }

        fileName = 'Backups/PSO' + str(numberOfDimenstions)
        fileName += "_G" + str(spawnerId)
        fileName += "_P" + str(len(particles))
        fileName += "_TMAX" + str(MAX_NUMBER_PER_GAME_PSO)
        fileName += "_C1-" + str(c1)
        fileName += "_C2-" + str(c2)
        fileName += "_W-"  + str(w)

        with open(fileName + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

Backup = BackupCreator()