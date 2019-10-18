import pygame

from consts    import *
from grid_cell import GridCell

class DisplayerBase:
    screen   = None
    color    = get_color(Colors.WHITE)
    position = None
    size     = FONT_SIZE

    def __init__(self, screen, position):
        self.screen   = screen
        self.position = position

    def draw_text(self, text, position, size =0):
        if size == 0 :
            font = pygame.font.SysFont("consolas", self.size)
        else:
            font = pygame.font.SysFont("consolas", size)

        text = font.render(str(text), True, self.color)
        text_rect = text.get_rect(center=(position[0], position[1]))
        self.screen.blit(text, text_rect)   

    def process(self): pass

    def empty_draw(self):
        pass

    def draw(self, smt):
        pass

class ScoreDisplayer(DisplayerBase):

    text = ""

    def __init__(self, screen, position):
        DisplayerBase.__init__(self, screen, position)     

    def draw(self):
        self.draw_text(   "Score", [( self.position[0] + self.size*5 ), ( self.position[1] + self.size       )]) 
        self.draw_text( self.text, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*2 + 3 )])

        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*3 ], 2)	

    def process(self, text):
        self.text = text


class NextTetiomerBox(DisplayerBase):
    grid     = None
    tetiomer = None
    CELL_GRID_HEIGHT = 3
    CELL_GRID_WIDTH  = 4

    def _init_grid(self):
        self.grid     = []
        for i in range(self.CELL_GRID_WIDTH):
            for j in range(self.CELL_GRID_HEIGHT):
                self.grid.append( GridCell(self.screen, ( self.position[0] + (i * SQUARE_SIZE) + self.size*3,  self.position[1] + (j * SQUARE_SIZE) + self.size*3 ) ) )

    def __init__(self, screen, position):
        DisplayerBase.__init__(self, screen, position)
        self._init_grid()

    def process(self, t):
        self.tetiomer = t

    def draw(self):
        self.draw_text("Next TETROMINO", [( self.position[0] + self.size*5 ), ( self.position[1] + self.size       )]) 
        self.fill_grid(self.tetiomer)
        for i in range(self.CELL_GRID_WIDTH*self.CELL_GRID_HEIGHT):
            self.grid[i].draw()

        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*8 ], 2)

    def _convert_id(self,a,b):
        return a * self.CELL_GRID_HEIGHT + b

    def fill_grid_for_O_Tetiomer(self,t):
            shape = t.get_shape()
            for a in range(self.CELL_GRID_WIDTH ):
                for b in range(self.CELL_GRID_HEIGHT ):
                    self.grid[self._convert_id(a,b)].fill_cell(get_color(Colors.BLACK))

            for a in range( 1,3,1):
                for b in range( 1,3,1):
                    self.grid[self._convert_id(a,b)].fill_cell(t.color)

    def fill_grid(self, t):
        if t is None : return
        if not t.can_rotate :
            self.fill_grid_for_O_Tetiomer(t)
            return

        shape = t.get_shape()
        for a in range(self.CELL_GRID_WIDTH ):
            for b in range(self.CELL_GRID_HEIGHT ):
                if shape[b][a] : self.grid[self._convert_id(a,b)].fill_cell(t.color)
                else: self.grid[self._convert_id(a,b)].fill_cell(get_color(Colors.BLACK))


    def empty_draw(self):
        self.color = get_color(Colors.LIGHT_PURPLE)
        self.draw_text("BLOCKED", [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*4  + 12  )]) 
        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*9 ], 2)

class HeuresticDisplayer(DisplayerBase):

    heuristics = [0,0,0,0,0,0,0]
    values     = [1,1,1,1]

    def __init__(self, screen, position):
        DisplayerBase.__init__(self, screen, position)     

    def process(self, heuristics, values):
        self.heuristics = heuristics
        self.values     = values

    def draw(self):
        heights  = "H : "
        heurVals = "Holes :" + str(self.heuristics[1]) + " H_sum :" + str(self.heuristics[2]) + " Bump :" + str(self.heuristics[3])
        for h in self.heuristics:
            heights += str(h) + " "

        t1 = "Hole rate :" + str(round(self.values[0], 3)) 
        t2 = "Sum rate  :" + str(round(self.values[1], 3))
        t3 = "Bump rate :" + str(round(self.values[2], 3)) 
        t4 = "Row rate  :" + str(round(self.values[3], 3))

        self.draw_text( heights , [( self.position[0] + self.size*5 ), ( self.position[1] + self.size       )], 12) 
        self.draw_text( heurVals, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*2 + 3 )], 16)
        self.draw_text( t1, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*3 + 3 )], 16)
        self.draw_text( t2, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*4 + 3 )], 16)
        self.draw_text( t3, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*5 + 3 )], 16)
        self.draw_text( t4, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*6 + 3 )], 16)

        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*7 ], 2)			
