from enum   import Enum
from Libraries.consts import *
import copy

class Tetromino:
    m_id            = 0
    shape           = [[],[],[],[]]
    previous_rotate = 0
    current_rotate  = 0
    max_rotate      = 0
    can_rotate      = True
    color           = get_color(Colors.BLACK)
    position        = [0,0] 
    prev_pos        = [0,0]

    position_range  = [0,0]

    enabled_size   = [0,0,0,0]

    is_locked      = False

    def __init__(self):
        
        self.shape           = [[],[],[],[]]
        self.previous_rotate = 0
        self.current_rotate  = 0
        self.max_rotate      = 0
        self.m_id            = 0
        self.enabled_size    = [0,0,3,3]
        self.position_range  = [0, GRID_WIDTH - self.enabled_size[2]]
        self.prev_pos        = [0,0]

    def rotate_left(self):
        if not self.can_rotate : return 
        self.previous_rotate = self.current_rotate
        self.current_rotate  = ( self.current_rotate - 1 ) if self.current_rotate - 1 >= 0 else self.max_rotate - 1
        self.prev_pos = self.position
        if self.position[0] < self.get_position_range()[0] : self.position[0] = self.get_position_range()[0]
        if self.position[0] > self.get_position_range()[1] : self.position[0] = self.get_position_range()[1]

    def rotate_right(self):
        if not self.can_rotate : return 
        self.previous_rotate = self.current_rotate
        self.current_rotate  = ( self.current_rotate + 1 ) if self.current_rotate + 1 < self.max_rotate else 0
        self.prev_pos = self.position
        if self.position[0] < self.get_position_range()[0] : self.position[0] = self.get_position_range()[0]
        if self.position[0] > self.get_position_range()[1] : self.position[0] = self.get_position_range()[1]

    def get_shape(self):
        return self.shape[self.current_rotate]

    def get_previous_shape(self):
        return self.shape[self.previous_rotate]

    def get_size(self):
        return self.enabled_size

    def revert_rotation(self):
        self.current_rotate = self.previous_rotate
        self.position[0]    = self.prev_pos[0]

    def get_position_range(self):
        return self.position_range

    def copy(self):
        return copy.copy(self)

    def is_valid(self, grid):
        #fall test
        if self.position[1] + self.get_size()[3] > GRID_HEIGHT: return False
        #fill test
        for i in range(self.get_size()[0], self.get_size()[2], 1):
            for j in range(self.get_size()[1], self.get_size()[3], 1):
            #    if self.position[1] 
                if self.get_shape()[j][i] and grid[self.position[0] + i][ self.position[1] + j] != 0:
                    return False
        return True


class O(Tetromino):

    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 1
        self.position        = [0,0] 
        self.can_rotate = False
        self.shape[0]  = [ [ 1, 1, 0, 0],
                           [ 1, 1, 0, 0],
                           [ 0, 0, 0, 0],
                           [ 0, 0, 0, 0]  ]
        self.max_rotate = 1
        self.color = get_color(Colors.LIGHT_BLUE)
        self.enabled_size   = [0,0,2,2]
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]

class T(Tetromino):

    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 2
        self.position        = [0,0] 


        self.shape[0] = [ [ 0, 1, 0, 0],
                          [ 1, 1, 1, 0],
                          [ 0, 0, 0, 0],
                          [ 0, 0, 0, 0] ]

        self.shape[1] = [ [ 0, 1, 0, 0],
                          [ 0, 1, 1, 0],
                          [ 0, 1, 0, 0],
                          [ 0, 0, 0, 0]  ]

        self.shape[2] = [ [ 0, 0, 0, 0],
                          [ 1, 1, 1, 0],
                          [ 0, 1, 0, 0],
                          [ 0, 0, 0, 0] ]

        self.shape[3] = [ [ 0, 1, 0, 0],
                          [ 1, 1, 0, 0],
                          [ 0, 1, 0, 0],
                          [ 0, 0, 0, 0]  ]

        self.rotate_center   = (1, 1) 
        self.max_rotate      = 4
        self.current_rotate  = 0
        self.color = get_color(Colors.GRAY)
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]

    def get_position_range(self):
        if self.current_rotate == 3 : return [ 0 ,GRID_WIDTH - self.enabled_size[2] + 1]  
        if self.current_rotate == 1 : return [-1 ,GRID_WIDTH - self.enabled_size[2]]  
        return self.position_range

    def get_size(self):
        if self.current_rotate == 0: return [0,0,3,2] 
        return self.enabled_size

class J(Tetromino):
    
    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 3
        self.position        = [0,0] 


        self.shape[0] = [ 
                          [0, 0, 1, 0],
                          [1, 1, 1, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0] ]

        self.shape[1] = [ [0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0] ]

        self.shape[2] = [ [0, 0, 0, 0],
                          [1, 1, 1, 0],
                          [1, 0, 0, 0],
                          [0, 0, 0, 0] ]

        self.shape[3] = [ [1, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0] ]
        self.rotate_center   = (1, 1) 
        self.max_rotate      = 4
        self.current_rotate  = 0
        self.color = get_color(Colors.DARK_VIOLET)
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]

    def get_position_range(self):
        if self.current_rotate == 3 : return [ 0 ,GRID_WIDTH - self.enabled_size[2] + 1]  
        if self.current_rotate == 1 : return [-1 ,GRID_WIDTH - self.enabled_size[2]]  
        return self.position_range

    def get_size(self):
        if self.current_rotate == 0: return [0,0,3,2] 
    #    if self.current_rotate == 2: return [0,0,2,3] 
        return self.enabled_size

class L(Tetromino):
    
    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 4
        self.position        = [0,0] 

        self.shape[0] = [ [1, 0, 0, 0],
                          [1, 1, 1, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0] ]

        self.shape[1] = [ [0, 1, 1, 0],
                          [0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0] ]

        self.shape[2] = [ [0, 0, 0, 0],
                          [1, 1, 1, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 0] ]

        self.shape[3] = [ [0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [1, 1, 0, 0],
                          [0, 0, 0, 0] ]



        self.rotate_center   = (1, 1) 
        self.max_rotate      = 4
        self.current_rotate  = 0
        self.color = get_color(Colors.YELLOW)
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]

    def get_position_range(self):
        if self.current_rotate == 1 : return [-1,GRID_WIDTH - self.enabled_size[2]]  
        if self.current_rotate == 3 : return [0,GRID_WIDTH - self.enabled_size[2] + 1]  
        return self.position_range

    def get_size(self):
        if self.current_rotate == 0: return [0,0,3,2] 
        return self.enabled_size

class Z(Tetromino):
    
    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 5
        self.position        = [0,0] 
        self.shape[0] = [ [ 0, 0, 0, 0 ],
                          [ 1, 1, 0, 0 ],
                          [ 0, 1, 1, 0 ],
                          [ 0, 0, 0, 0 ] ]

        self.shape[1] = [ [ 0, 0, 1, 0 ],
                          [ 0, 1, 1, 0 ],
                          [ 0, 1, 0, 0 ],
                          [ 0, 0, 0, 0 ] ]
        self.rotate_center   = (1, 1) 
        self.current_rotate  = 0
        self.max_rotate      = 2
        self.color = get_color(Colors.GREEN)
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]

    def get_position_range(self):
        if self.current_rotate == 1 : return [-1,GRID_WIDTH - self.enabled_size[2]]  
        return self.position_range

class I(Tetromino):
    
    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 6
        self.position        = [0,0] 
        self.shape[0] = [ [ 0, 0, 0, 0 ],
                          [ 1, 1, 1, 1 ],
                          [ 0, 0, 0, 0 ],
                          [ 0, 0, 0, 0 ] ]

        self.shape[1] = [ [ 0, 1, 0, 0 ],
                          [ 0, 1, 0, 0 ],
                          [ 0, 1, 0, 0 ],
                          [ 0, 1, 0, 0 ] ]

        self.rotate_center   = (1, 1) 
        self.current_rotate  = 0
        self.max_rotate      = 2
        self.color = get_color(Colors.RED)
        self.enabled_size = [0,0,4,4]
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]

    def get_position_range(self):
        if self.current_rotate == 0 : return [ 0,GRID_WIDTH - self.enabled_size[2]]  
        if self.current_rotate == 3 : return [-2,GRID_WIDTH - self.enabled_size[2] + 1]  
        if self.current_rotate == 2 : return [ 0,GRID_WIDTH - self.enabled_size[2]]  
        if self.current_rotate == 1 : return [-1,GRID_WIDTH - self.enabled_size[2] + 2]  
        return self.position_range

    def get_size(self):
        if self.current_rotate == 0: return [0,0,4,2] 
        if self.current_rotate == 2: return [0,0,4,3] 
        return self.enabled_size

class N(Tetromino):
    
    def __init__(self):
        Tetromino.__init__(self)
        self.m_id = 7
        self.position        = [0,0] 
        self.shape[0] = [ [ 0, 0, 0, 0 ],
                          [ 0, 1, 1, 0 ],
                          [ 1, 1, 0, 0 ],
                          [ 0, 0, 0, 0 ] ]

        self.shape[1] = [ [ 0, 1, 0, 0 ],
                          [ 0, 1, 1, 0 ],
                          [ 0, 0, 1, 0 ],
                          [ 0, 0, 0, 0 ] ]
        self.rotate_center   = (1, 1) 
        self.current_rotate  = 0
        self.max_rotate      = 2
        self.color = get_color(Colors.BLUE)
        self.position_range = [0,GRID_WIDTH - self.enabled_size[2]]
        
    def get_position_range(self):
        if self.current_rotate == 1 : return [-1,GRID_WIDTH - self.enabled_size[2]]  
        return self.position_range

class Tetrominos(Enum):
    O = O()
    N = N()
    I = I()
    Z = Z()
    T = T()
    J = J()
    L = L()