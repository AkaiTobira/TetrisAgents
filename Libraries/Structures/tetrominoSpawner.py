from Libraries.Structures.tetiomers import O, N, Z, T, J, L, I
from random import shuffle

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


