from Libraries.Structures.tetiomers import O, N, Z, T, J, L, I
from random import random, shuffle
from Libraries.Algoritms.alg_evolution import EvolutionAlgoritm
import json
class SimpleSpawnTetrimino:
    c_tetromino = None
    n_tetromino = None

    tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
    index       = 0

    def __init__(self):
        self.tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
        shuffle(self.tetrominos)
        self.c_tetromino = self.tetrominos[0]

        self.tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
        shuffle(self.tetrominos)
        self.n_tetromino = self.tetrominos[0]

    def get_next(self):
        self.c_tetromino = self.n_tetromino
        self.tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
        shuffle(self.tetrominos)
        self.n_tetromino = self.tetrominos[0]

    def reset(self):
        self.__init__()

    def disable(self): pass

class RandomSpawnTetromino:
    c_tetromino = None
    n_tetromino = None

    tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
    index       = 0

    def __init__(self):
        shuffle(self.tetrominos)
        self.c_tetromino = self.tetrominos[0]
        self.n_tetromino = self.tetrominos[1]
        self.index       = 1

    def increment_index(self):
        self.index = (self.index+1) % 7

    def get_next(self):
        self.c_tetromino = self.n_tetromino
        self.increment_index()
        self.n_tetromino = self.tetrominos[self.index]
        
        if self.index == 0:
            #self.tetrominos = [O(),O(),O(),O(),O(),O(),O()]
            self.tetrominos = [ O(), N(),  Z(), T(), J(), L(), I()]
            shuffle(self.tetrominos)

    def reset(self):
        self.tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
        shuffle(self.tetrominos)
        self.index = 6
        self.get_next()

    def disable(self): pass

class NewestRandomSpawnTetromino:
    c_tetromino = None
    n_tetromino = None

    tetrominos = [ 
        1,1,1,1,1,
        2,2,2,2,2,
        3,3,3,3,3,
        4,4,4,4,4,
        5,5,5,5,5,
        6,6,6,6,6,
        7,7,7,7,7
        ]

    memory = [1,2,3,4]

    def _get_tetrimino_by_index(self, index):
        return {
        1: O(),
        2: T(),
        3: J(),
        4: L(),
        5: Z(),
        6: I(),
        7: N()
    }[index]

    def _get_random_index(self):
        return int(random() * len( self.tetrominos))

    def __init__(self):
        self.reset()

    def _get_next_tetrimino_internal(self):
        randomValue = self._get_random_index()

        tetriminoIndex = self.tetrominos[randomValue]
        self.tetrominos[randomValue] = self.tetrominos[len(self.tetrominos)-1]

        if tetriminoIndex in self.memory:
            self.memory.remove(tetriminoIndex)
        self.memory.append(tetriminoIndex)

        self.tetrominos[len(self.tetrominos)-1] = self.memory[0]
        return self._get_tetrimino_by_index(tetriminoIndex)

    def get_next(self):
        self.c_tetromino = self.n_tetromino
        self.n_tetromino = self._get_next_tetrimino_internal()

    def reset(self):
        self.tetrominos = [ 
            1,1,1,1,1,
            2,2,2,2,2,
            3,3,3,3,3,
            4,4,4,4,4,
            5,5,5,5,5,
            6,6,6,6,6,
            7,7,7,7,7
            ]
        self.memory = [1,2,3,4]
        self.c_tetromino = self._get_next_tetrimino_internal()
        self.n_tetromino = self._get_next_tetrimino_internal()

    def disable(self): pass

class NewestRandomSpawnTetriminoLocked:

    spawner = NewestRandomSpawnTetromino()
    currentTetriminoSet = None
    tetriminoIndex = 0
    gameIndex = 0
    c_tetromino = None
    n_tetromino = None

    def _get_tetrimino_by_index(self, index):
        return {
        1: O(),
        2: T(),
        3: J(),
        4: L(),
        5: Z(),
        6: I(),
        7: N()
    }[index]


    def reset(self):
        self.gameIndex = (self.gameIndex + 1)%EvolutionAlgoritm.NUMBER_OF_PLAYED_GAMES

        with open('Backups/Generator/Game_' + str(self.gameIndex) +  '.json') as json_file:
            self.currentTetriminoSet = json.loads(json_file.read())
        
        self.tetriminoIndex = 0
        self.c_tetromino = self._get_tetrimino_by_index(self.currentTetriminoSet[0])
        self.n_tetromino = self._get_tetrimino_by_index(self.currentTetriminoSet[1])

    def get_next(self):
        self.tetriminoIndex += 1
        self.c_tetromino = self._get_tetrimino_by_index(self.currentTetriminoSet[self.tetriminoIndex])
        self.n_tetromino = self._get_tetrimino_by_index(self.currentTetriminoSet[self.tetriminoIndex+1])

    def __init__(self ):
        try:
            with open('Backups/Generator/Game_0.json') as json_file:
                if json_file == None: raise IOError
                self.currentTetriminoSet = json.loads(json_file.read())
        except IOError:
            self.create_base()
            with open('Backups/Generator/Game_0.json') as json_file:
                self.currentTetriminoSet = json.loads(json_file.read())




        self.c_tetromino = self._get_tetrimino_by_index(self.currentTetriminoSet[0])
        self.n_tetromino = self._get_tetrimino_by_index(self.currentTetriminoSet[1])

       # with open('logs/bestBackup.json') as json_file:
        #    self.json_converted = json.loads(json_file.read())

    def disable(self): pass

    def create_base(self):
        for i in range(8):
            with open('Backups/Generator/Game_' + str(i) +  '.json', 'w') as outfile:
                game = []
                for i in range(10000):
                    self.spawner.get_next()
                    game.append(self.spawner.n_tetromino.m_id)
                json.dump(game, outfile, indent=4)
        

fff = NewestRandomSpawnTetriminoLocked()

class MultipleSpawnTetromino:
    c_tetromino = None
    n_tetromino = None

    getFunction  = None
    resetSpawner = None
    disabled = None
    spawnerId   = 0

    def __init__(self, spawnerId, getFunction, resetSpawner, disablee):
        self.getFunction = getFunction
        self.resetSpawner = resetSpawner
        self.disabled      = disablee
        self.spawnerId   = spawnerId


    def get_next(self):
        self.c_tetromino, self.n_tetromino = self.getFunction(self.spawnerId)

    def reset(self):
        self.resetSpawner(self.spawnerId)

    def setFirstTwo(self, listt):
        self.c_tetromino, self.n_tetromino = listt[0], listt[1]

    def disable(self):
        self.disabled(self.spawnerId)

class MultiRandomSpawner:
    number_of_spawners   = 0
    randomSpawner        = None
    tetromino_base_id    = 0
    tetromino_track      = []
    tetromino_track_list = { }

    spawners = []

    def __init__(self, playerNumber):
        self.randomSpawner = RandomSpawnTetromino()
        self.number_of_spawners = playerNumber

        for i in range(playerNumber):
            self.tetromino_track_list[i] = { "cleaned" : 
            [ self.randomSpawner.c_tetromino.copy(), 
              self.randomSpawner.n_tetromino.copy() ], "isActive" : True }
            self.spawners.append( MultipleSpawnTetromino( i, self.get_next, self.reset, self.playerGameOver))

        for i in range(playerNumber):
            self.spawners[i].setFirstTwo( self.tetromino_track_list[i]["cleaned"] )

    def playerGameOver(self, playerId):
        self.tetromino_track_list[playerId]["isActive"] = False

    def reset(self, index):
        self.randomSpawner = RandomSpawnTetromino()
        for i in range(self.number_of_spawners):
            self.tetromino_track_list[i] = { "cleaned" : 
            [ self.randomSpawner.c_tetromino.copy(), 
              self.randomSpawner.n_tetromino.copy() ], "isActive" : True }

    def get_spawner(self, index):
        return self.spawners[index]

    def get_next(self, playerId): 
        self.tetromino_track_list[playerId]["cleaned"] = self.tetromino_track_list[playerId]["cleaned"][1:]
        if len(self.tetromino_track_list[playerId]["cleaned"]) == 1: self.add_to_all()
        return self.tetromino_track_list[playerId]["cleaned"][0], self.tetromino_track_list[playerId]["cleaned"][1]

    def add_to_all(self):
        self.randomSpawner.get_next()
        for i in range(self.number_of_spawners):
            if self.tetromino_track_list[i]["isActive"]:
                self.tetromino_track_list[i]["cleaned"].append(self.randomSpawner.n_tetromino.copy())
