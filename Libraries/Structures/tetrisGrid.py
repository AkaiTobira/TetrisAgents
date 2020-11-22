
from Libraries.consts import *
from copy import deepcopy

class MoveMeasures:
    pass
## TODO Dropped for now
class TetrisGridNew:
    grid = []

    backup_grid_changed = { }


    def __init__(self):
        for i in range(GRID_WIDTH):
            self.grid.append([])
            for j in range(GRID_HEIGHT):
                self.grid[i].append(0)

    def place_tetromino(self, tetromino):
        shape_size = tetromino.get_size()
        shape      = tetromino.get_shape()
        pos        = tetromino.position

        if tetromino.is_locked : return

        self._store_backup( range(shape_size[0], shape_size[2], 1) )

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i]: self.grid[pos[0] + i][ pos[1] + j] = tetromino.m_id

    def _store_backup(self, _range ):
        backup_grid_changed = {}
        for i in _range:
            # To check if deepCopy
            self.backup_grid_changed[pos[0] + i] = self.grid[pos[0] + i]


# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000
# 000000000000000000000000000

    #def measure(self):


