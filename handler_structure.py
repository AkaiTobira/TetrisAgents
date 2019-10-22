
import pprint
from random import randint
from tetiomers  import *

lis = [ N(), Z(), O(), J(), L(), T(), I()]

class MultidimensionalDictionary:
    _dict = {}
    _size = 0
    _range_size = 0
    _fragment   = []
    alpha = 0.1

    def __convert_tetromino_to_index(self, tetromino):
        if type(tetromino) == O : return 2
        if type(tetromino) == L : return 4
        if type(tetromino) == J : return 3
        if type(tetromino) == N : return 0
        if type(tetromino) == Z : return 1
        if type(tetromino) == T : return 5
        if type(tetromino) == I : return 6

    def __init__(self, size, _range ):
        self._dict = {}
        self._size = size
        self._range_size = _range[0] * -1
        print( self._range_size)
        self._build_dictionary( _range)

    def _build_dictionary(self,  _range):
        for obj in lis:
            index = self.__convert_tetromino_to_index(obj)
            self._dict[ index ] = {}
            for rot in range(obj.max_rotate):
                self._dict[ index ][rot] = {}
                self._fill_row(self._dict[ index ][rot], 0, _range)

    def _fill_row(self, row, current_size, _range):
        if self._size - 1 == current_size: 
            for i in _range: row[i] = [0,0]
            return

        for i in _range:
            row[i] = {}
            self._fill_row( row[i], current_size + 1, _range)

    def get_value(self, tetromino, situation):
        probs     = self._dict[self.__convert_tetromino_to_index(tetromino)][tetromino.current_rotate]
        max_shift = 10 - self._size

        best          = -100
        self._fragment      = []
        best_position = -1

        for shift in range(max_shift):
            probs_holder = probs
            for s in range(shift, self._size + shift, 1):

                if situation[s] < -self._range_size: situation[s] = -self._range_size
                if situation[s] >  self._range_size: situation[s] =  self._range_size

                sit = situation[s]

                probs_holder = probs_holder[sit]

            position     = shift  if probs_holder[0] > probs_holder[1] else self._size + shift -1
            holder = probs_holder[0] if probs_holder[0] > probs_holder[1] else probs_holder[1]

            if holder > best:
                best           = holder
                self._fragment = [self.__convert_tetromino_to_index(tetromino), tetromino.current_rotate] + situation[ shift : self._size + shift ] +[ 0 if probs_holder[0] > probs_holder[1] else 1 ]
                best_position  = position

        return [best, tetromino.current_rotate, best_position]

    def get_random_value(self, tetromino, situation):
        probs     = self._dict[self.__convert_tetromino_to_index(tetromino)][randint(0, tetromino.max_rotate-1)]
        max_shift = 10 - self._size

        self._fragment      = []

        shift = randint(0,max_shift-1)
        probs_holder = probs
        print( range(shift, self._size + shift, 1) )
        for s in range(shift, self._size + shift, 1):
            
            if situation[s] < -self._range_size: situation[s] = -self._range_size
            if situation[s] >  self._range_size: situation[s] =  self._range_size

            sit = situation[s]

            probs_holder = probs_holder[sit]

        last_index   = randint(0,1)
        position     = shift           if last_index == 0 else self._size + shift -1
        holder       = probs_holder[0] if last_index == 0 else probs_holder[1]

        self._fragment = [self.__convert_tetromino_to_index(tetromino), tetromino.current_rotate] + situation[ shift : self._size + shift ] +[ last_index ]
        
        return [holder, tetromino.current_rotate, position]



    def update(self, value):
        val2  = self._dict
        val   = self._dict
        print( self._fragment )
        for s in self._fragment:
            val2 = val
            print( s, end=" ")
            val = val[s]
        val2[self._fragment[len(self._fragment)-1]] += self.alpha * ( value - val)
            





            #print( " : ", probs_holder)

        #todo : save best result in something
        #todo : update haved index


temp = MultidimensionalDictionary(4, (-2,-1, 0, 1, 2))

tetromino          = lis[ randint(0, len(lis)-1 )]
tetromino.curr_rot = randint(0, tetromino.max_rotate)

print( temp.get_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1]) )
temp.update( 100 )
print( temp.get_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1]) )


