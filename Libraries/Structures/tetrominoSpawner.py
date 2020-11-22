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




# TODO : Dodać pobieranie z jednej listy, na której przechowywane są wszysktie klocki od początku gry
# potem aktualiowanie indexu i czyszczenie tablicy z ostatniego klocka
#
class MultiRandomSpawner:
    number_of_spawners   = 0
    randomSpawner        = None
    tetromino_base_id    = 0
    tetromino_track      = []
    tetromino_track_list = { }

    def __init__(self, playerNumber):
        self.randomSpawner = RandomSpawnTetromino()

        for i in range(playerNumber):
            self.tetromino_track_list[i] = { "cleaned" : 0, "isActive" : True }

    def get_next(slef, playerId):
        if self.tetromino_track_list[playerId]["isActive"] :
            return self.tetromino_track[ tetromino_track_list[playerId] - self.tetromino_base_id ]


    def playerGameOver(self, playerId):
        self.tetromino_track_list[playerId]["isActive"] = False

    


