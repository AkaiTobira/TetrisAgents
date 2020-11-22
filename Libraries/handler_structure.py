
import pprint
from random import randint
from Libraries.Structures.tetiomers  import *

lis = [ N(), Z(), O(), J(), L(), T(), I()]



class DictionaryBuilder:

    def __convert_tetromino_to_index(self, tetromino):
        if type(tetromino) == O : return 2
        if type(tetromino) == L : return 4
        if type(tetromino) == J : return 3
        if type(tetromino) == N : return 0
        if type(tetromino) == Z : return 1
        if type(tetromino) == T : return 5
        if type(tetromino) == I : return 6

    def build_dictionary(self,  _range, size):
        _dict = {}
        for obj in lis:
            index = self.__convert_tetromino_to_index(obj)
            _dict[ index ] = {}
            for rot in range(obj.max_rotate):
                _dict[ index ][rot] = {}
                self._fill_row(_dict[ index ][rot], size,  0, _range)
        return _dict

    def _fill_row(self, row, size,  current_size, _range):
        if size - 1 == current_size: 
            for i in _range: row[i] = [0,0]
            return

        for i in _range:
            row[i] = {}
            self._fill_row( row[i], size,  current_size + 1, _range)

class MultidimensionalDictionary:
    _dict                 = {}
    _size                 = 0
    _range_size           = 0
    _memorised_sequence   = []
    LEARNING_RATE         = 0.1
    NUMBER_OF_SUSEQUENCES = 0


    def __convert_tetromino_to_index(self, tetromino):
        if type(tetromino) == O : return 2
        if type(tetromino) == L : return 4
        if type(tetromino) == J : return 3
        if type(tetromino) == N : return 0
        if type(tetromino) == Z : return 1
        if type(tetromino) == T : return 5
        if type(tetromino) == I : return 6


    def __init__(self, size, _range ): pass
    #    self._dict = {}
     #   self._size = size
      #  self.NUMBER_OF_SUSEQUENCES = 10 - self._size
       # self._range_size = _range[0] * -1
        #self._dict = DictionaryBuilder().build_dictionary( _range, size)

    def get_value(self, tetromino, situation):
        teromino_index           = self.__convert_tetromino_to_index(tetromino)
        situation                = self.__normalize_sequence(situation)
        dict_of_actual_tetromino = self._dict[teromino_index][tetromino.current_rotate]
                                   #rate                             #position
        found_best               = [ -100, tetromino.current_rotate,       -10 ]
        self._memorised_sequence = []

        print( situation )

        for shift in range(self.NUMBER_OF_SUSEQUENCES):
            values_of_sequence = dict_of_actual_tetromino
            values_of_sequence = self.__get_values_of_sequence( values_of_sequence, shift, self._size + shift, situation)

            pos1 = shift + tetromino.get_position_range()[0] 
            pos2 = self._size + shift -1 + tetromino.get_position_range()[0] - tetromino.get_size()[2]

            print( pos1, pos2 )
            found_best, is_better = self.__rate_sequence(found_best,tetromino, values_of_sequence , pos1 , pos2)

            #print( pos1, pos2 )
            print( found_best )
            if is_better:
                self._memorised_sequence = [teromino_index, tetromino.current_rotate] + situation[ shift : self._size + shift ] + self._memorised_sequence


        print("selected ::: ", found_best )
        return found_best

    def __rate_sequence(self, found_best, tetromino ,values_of_sequence, first_position, second_position):

        #print( values_of_sequence )

                    #position        #rate                  #dictionaty value index
        sequence = [ first_position, values_of_sequence[0],                       0 ]
        
        if second_position <= tetromino.get_position_range()[1] and values_of_sequence[1] > values_of_sequence[0]:
            sequence = [ second_position, values_of_sequence[1], 1 ]

        is_better = False

        print( sequence, sequence[1], found_best, found_best[0] )

        if sequence[1] > found_best[0]:
            is_better = True
            self._memorised_sequence = [ sequence[2] ]
            found_best[0]            = sequence[1]
            found_best[2]            = sequence[0]

        return found_best, is_better

    def __random_sequence(self, found_best,tetromino, values_of_sequence, first_position, second_position):

        #print( values_of_sequence )

                    #position        #rate                  #dictionaty value index
        sequence = [ first_position, values_of_sequence[0],                       0 ]
        
        print(  second_position < tetromino.get_position_range()[1], tetromino.get_position_range()[1])
        print( tetromino.current_rotate, tetromino.get_position_range() )

        if randint(0,1) == 1 and second_position <= tetromino.get_position_range()[1] : 
            sequence = [ second_position, values_of_sequence[1],                       1 ]

        #print( "Best found ", found_best)

        is_better = False
        if sequence[1] > found_best[0]:
            is_better = True
            self._memorised_sequence = [ sequence[2] ]
            found_best[0]            = sequence[1]
            found_best[2]            = sequence[0]

        #print( "Best found ", found_best)

        return found_best, is_better

    def __normalize_sequence(self, sequence):
        for i in range( len(sequence)):
            if sequence[i] < -self._range_size: sequence[i] = -self._range_size
            if sequence[i] >  self._range_size: sequence[i] =  self._range_size
        return sequence

    def __get_values_of_sequence(self, start_point ,sequence_begin_index, sequence_end_index, sequence):
       # print( sequence_begin_index, sequence_end_index)
        print( sequence[0:sequence_end_index])
        for index in range(sequence_begin_index, sequence_end_index, 1):
            #print( index )
            #if index == sequence_end_index - 1: print( start_point )
            start_point = start_point[sequence[index]]
        return start_point

    def get_random_value(self, tetromino, situation):
        teromino_index = self.__convert_tetromino_to_index(tetromino)

        val = randint(0,12)
        for i in range(val): tetromino.rotate_left()
        situation = self.__normalize_sequence(situation)
        dict_of_actual_tetromino = self._dict[teromino_index][tetromino.current_rotate]
        
                                   #rate                             #position
        found_best               = [ -100, tetromino.current_rotate, -10 ]
        self._memorised_sequence = []

        shift = randint(0,self.NUMBER_OF_SUSEQUENCES-1)
        #print( shift )
        values_of_sequence = dict_of_actual_tetromino
        values_of_sequence = self.__get_values_of_sequence( values_of_sequence, shift, self._size + shift, situation)

        pos1 = shift + tetromino.get_position_range()[0]
        pos2 = self._size + shift + tetromino.get_position_range()[0]

        print( " position ", pos1, pos2)

        found_best, is_better = self.__random_sequence(found_best, tetromino, values_of_sequence , pos1 , pos2)
        
        print( "best found in random", found_best )

        if is_better:
                self._memorised_sequence = [teromino_index, tetromino.current_rotate] + situation[ shift : self._size + shift ] + self._memorised_sequence

        return found_best

    def __get_values_from_memory_track(self):
        val = self._dict
        for i in range( len(self._memorised_sequence) -1 ):
            val = val[ self._memorised_sequence[i]]
        return val

    def update(self, value):
        values_of_sequence = self.__get_values_from_memory_track()
        current_value      = values_of_sequence[self._memorised_sequence[len(self._memorised_sequence)-1]]
        values_of_sequence[ self._memorised_sequence[len(self._memorised_sequence)-1] ] += self.LEARNING_RATE * ( value - current_value)

#temp = MultidimensionalDictionary(4, (-2,-1, 0, 1, 2))
#
#tetromino                = lis[ randint(0, len(lis)-1 )]
#tetromino.current_rotate = randint(0, tetromino.max_rotate-1)
#
#print( temp.get_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1]) )
#temp.update( 100 )
#print( temp.get_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1]) )
#print( temp.get_random_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1]) )
#
#r = pprint.PrettyPrinter()
#
#r.pprint(temp._dict)
#
#
#print( "test basic")
#for i in range( 1000 ):
#    tetromino = lis[ randint(0, len(lis)-1) ];
#    tetromino.current_rotate = randint(0, tetromino.max_rotate-1)
#    a = temp.get_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1])
#
#    if a[2] < tetromino.get_position_range()[0] or a[2] > tetromino.get_position_range()[1]:
#        print( a, tetromino.get_position_range(), tetromino.current_rotate, tetromino )
#        raise Exception('spam', 'eggs')
#
#print( "test rANDOM     ")
#for i in range( 1000 ):
#    tetromino = I();
#    tetromino.current_rotate = randint(0, tetromino.max_rotate-1)
#    a = temp.get_random_value( tetromino, [2,-1,-1,3,-4,1,0,3,-1])
#
#    if a[2] < tetromino.get_position_range()[0] or a[2] > tetromino.get_position_range()[1]:
#        print( a, tetromino.get_position_range(), tetromino.current_rotate, tetromino )
#        raise Exception('spam', 'eggs')
#