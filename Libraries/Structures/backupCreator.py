
from Libraries.consts import *
from Libraries.vector import Vector
from Libraries.Algoritms.particle import Particle
from Libraries.Structures.settings import PARAMS
from keras.models     import Sequential, save_model, load_model
from collections import deque

import json

class BackupCreator:
    particles = { 4 : [], 5 :[], 6 :[],  7 :[], 10:[] }

    def __init__(self): pass

    def save_neural_network(self, instance):
        backup = {
            "date_time"  : instance.dateTime,
            "model_path" : "Backups/Networks/" + instance.NAME,
            "epsilon"    : instance.epsilon,
            "discount"   : instance.discount,
            "memory"     : list(instance.memory)
        }

        instance.model.save(backup["model_path"])

        with open('Backups/' +instance.NAME +'.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

    def load_neural_network(self, instance):
        json_converted = None

        try:
            with open('Backups/' + str(instance.NAME) +  '.json', "r") as json_file:
                json_converted = json.loads(json_file.read())
        except IOError:
            return False

        instance.model    = load_model( json_converted["model_path"])
        instance.memory   = deque(json_converted["memory"], maxlen=PARAMS.MAX_POINTS)
        instance.discount = json_converted["discount"]
        instance.epsilon  = json_converted["epsilon"]
        instance.dateTime = json_converted["date_time"]
        return True

    def load_evolution(self, instance):
        json_converted = None

        try:
            with open('Backups/' + instance.NAME + '.json', 'r') as json_file:
                json_converted = json.loads(json_file.read())
        except IOError:
            print("No valid backup for :" + instance.NAME)
            return False

        if json_converted["reset"]: 
            print("Reseting backup")
            return False

        dimensions = PARAMS.HEURYSTIC_AMOUNT
        instance.population      = []
        for i in range( len( json_converted["population"]) ):
            vec = Vector(dimensions)
            vec.v =  json_converted["population"][i]["values"]
            instance.population.append( [ vec, json_converted["population"][i]["score"]] )

        instance.parents         = []
        for i in range( len( json_converted["parents"]) ):
            vec = Vector(dimensions)
            vec.v =  json_converted["parents"][i]["values"]
            instance.parents.append( [ vec, json_converted["parents"][i]["score"]] )

        instance.prev_population = []
        for i in range( len( json_converted["p_population"]) ):
            vec = Vector(dimensions)
            vec.v =  json_converted["p_population"][i]["values"]
            instance.prev_population.append( [ vec, json_converted["p_population"][i]["score"]] )

        instance.unchecked_population = []
        for i in range( len( json_converted["to_check"]) ):
            vec = Vector(dimensions)
            vec.v =  json_converted["to_check"][i]["values"]
            instance.unchecked_population.append( [vec, 0] )

        instance.generation    = json_converted["generation"]
        instance.dateTime      = json_converted["date_time"]
        PARAMS.ELITARY_SELECT = json_converted["mutation_rate"]
        PARAMS.MUTATION_RATE = json_converted["elythys_rate"]
        instance.best_found    = json_converted["best_found"]
        instance.avrg_tetriminos = json_converted["avg"]

        print('Backups/' + instance.NAME + ": Backup Loaded")
        return True

    def save_evolution(self, instance):
        backup = {
            "generation"      : instance.generation,
            "date_time"       : instance.dateTime,
            "number_of_tetrominos_per_game" : PARAMS.MAX_POINTS,
            "left_to_process" : len(instance.unchecked_population),
            "number_of_games" : PARAMS.NUMBER_OF_GAMES,
            "reset"           : False,
            "population_size" : len(instance.population),
            "mutation_rate"   : PARAMS.MUTATION_RATE,
            "elythys_rate"    : PARAMS.ELITARY_SELECT,
            "best_found"      : [instance.best_found[0], instance.best_found[1]],
            "avg"             : instance.avrg_tetriminos,

            "population"      : [],
            "to_check"        : [],
            "parents"         : [],
            "p_population"    : []
        }

        for i in range( len(instance.population) ):
            backup["population"].append( {
                "score"  : instance.population[i][1],
                "values" : instance.population[i][0].v
            })

        for i in range( len(instance.unchecked_population) ):
            backup["to_check"].append( {
                "values" : instance.unchecked_population[i][0].v
            })

        for i in range( len(instance.parents) ):
            backup["parents"].append( {
                "score"  : instance.parents[i][1],
                "values" : instance.parents[i][0].v
            })

        for i in range( len(instance.prev_population) ):
            backup["p_population"].append( {
                "score"  : instance.prev_population[i][1],
                "values" : instance.prev_population[i][0].v
            })

        with open('Backups/' + instance.NAME + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

    def load_pso(self, pso_instance):
        json_converted = None
        filename = 'Backups/' + pso_instance.NAME
        try:
            with open(filename + '.json', 'r') as json_file:
                json_converted = json.loads(json_file.read())
        except IOError:
            print("No valid backup instance for filename=" + filename)
            return False

        pso_instance.particles = []
        for i in range( PARAMS.POPULATION_SIZE ):
            part = Particle( nmberOfDimension=PARAMS.HEURYSTIC_AMOUNT, curr_score=json_converted["particles"][i]["curr_score"])
            part.dir_v.v    = json_converted["particles"][i]["dir_v"]
            part.pos_v.v    = json_converted["particles"][i]["pos_v"]
            part.best_pos.v = json_converted["particles"][i]["best_pos"]
            part.curr_score = json_converted["particles"][i]["curr_score"]
            part.best_score = json_converted["particles"][i]["best_score"] 
            pso_instance.particles.append( part )

        pso_instance.iteraiton = json_converted["iteration"] 
        pso_instance.dateTime  = json_converted["date_time"]
        pso_instance.index     = json_converted["current_index"]

        pso_instance.best_pos   = Vector(PARAMS.HEURYSTIC_AMOUNT)
        pso_instance.best_pos.v = json_converted["best_particle_pos"]
        pso_instance.best_score = json_converted["best_score"]
        return True

    def save_pso(self, pso_instance):
        backup = {
            "date_time"         : pso_instance.dateTime,
            "iteration"         : pso_instance.iteration,
            "c1"                : PARAMS.C1,
            "c2"                : PARAMS.C2,
            "w"                 : PARAMS.W,
            "current_index"     : pso_instance.index,
            "best_particle_pos" : pso_instance.best_pos.v,
            "best_score"        : pso_instance.best_score,
            "particles_number"  : PARAMS.POPULATION_SIZE,
            "number_of_tetrominos_per_game" : PARAMS.MAX_POINTS,
            "particles"         : []
        }

        for i in range( PARAMS.POPULATION_SIZE ):
            backup["particles"].append({
                "dir_v"      : pso_instance.particles[i].dir_v.v,
                "pos_v"      : pso_instance.particles[i].pos_v.v,
                "best_pos"   : pso_instance.particles[i].best_pos.v,
                "best_score" : pso_instance.particles[i].best_score,
                "curr_score" : pso_instance.particles[i].curr_score
            })
        
        fileName = 'Backups/' + pso_instance.NAME
        with open(fileName + '.json', 'w') as outfile:
            json.dump(backup, outfile, indent=4)

Backup = BackupCreator()