import pygame

from Libraries.consts    import *
from Libraries.Structures.grid_cell import GridCell
from Libraries.Structures.fps_counter import FPSCounter

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

class FPSDisplayer:
    screen   = None
    color    = get_color(Colors.WHITE)
    position = None
    counter  = FPSCounter()

    size     = FONT_SIZE

    def __init__(self, screen, position):
        self.screen   = screen
        self.position = position

    def update(self, delta):
        self.counter.update(delta)

    def draw_text(self, size =0):
        if size == 0 :
            font = pygame.font.SysFont("consolas", self.size)
        else:
            font = pygame.font.SysFont("consolas", size)
    
        text = font.render("MPS:" + self.counter.getFPS(), True, self.color)
        text_rect = text.get_rect(center=(self.position[0], self.position[1]))
        self.screen.blit(text, text_rect) 

class ScoreDisplayer(DisplayerBase):

    text = ""

    def __init__(self, screen, position):
        DisplayerBase.__init__(self, screen, position)     

    def draw(self):
        self.draw_text(   "Score", [( self.position[0] + self.size*5 ), ( self.position[1] + self.size + 10  )], 12) 
        self.draw_text( self.text, [( self.position[0] + self.size*5 ), ( self.position[1] + self.size + 25 )])

    #    pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*2 ], 2)	

    def process(self, text):
        self.text = text

#TODO optimalization
class NextTetiomerBox(DisplayerBase):
    grid     = None
    tetiomer = None


    def _init_grid(self):
        self.grid     = []
        for i in CELL_GRID_WIDTH:
            for j in CELL_GRID_HEIGHT:
                self.grid.append( GridCell(self.screen, ( self.position[0] + (i * SQUARE_SIZE) + self.size*3,  self.position[1] + (j * SQUARE_SIZE) + self.size*3 ) ) )

    def __init__(self, screen, position):
        DisplayerBase.__init__(self, screen, position)
        self._init_grid()

    def process(self, t):
        self.tetiomer = t

    def draw(self):
        self.draw_text("Next TETROMINO", [( self.position[0] + self.size*5 ), ( self.position[1] + self.size       )]) 
        self.fill_grid(self.tetiomer)
        for i in CELL_GRID_BOTH:
            self.grid[i].draw()

        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*8 ], 2)

    def _convert_id(self,a,b):
        return a * 3 + b

    def fill_grid_for_O_Tetiomer(self,t):
            shape = t.get_shape()
            for a in CELL_GRID_WIDTH:
                for b in CELL_GRID_HEIGHT:
                    self.grid[self._convert_id(a,b)].fill_cell(get_color(Colors.BLACK))

            for a in RANGE_1_3:
                for b in RANGE_1_3:
                    self.grid[self._convert_id(a,b)].fill_cell(t.color)

    def fill_grid(self, t):
        if t is None : return
        if not t.can_rotate :
            self.fill_grid_for_O_Tetiomer(t)
            return

        shape = t.get_shape()
        for a in CELL_GRID_WIDTH:
            for b in CELL_GRID_HEIGHT:
                if shape[b][a] : self.grid[self._convert_id(a,b)].fill_cell(t.color)
                else: self.grid[self._convert_id(a,b)].fill_cell(get_color(Colors.BLACK))


    def empty_draw(self):
        self.color = get_color(Colors.LIGHT_PURPLE)
        self.draw_text("BLOCKED", [( self.position[0] + self.size*5 ), ( self.position[1] + self.size*4  + 12  )]) 
        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*9 ], 2)

class HeuresticDisplayer(DisplayerBase):

    grid = None
    heuristics = [0,0,0,0,0,0,0]
    values     = [1,1,1,1]

    def __init__(self, screen, position, grid):
        DisplayerBase.__init__(self, screen, position)     
        self.grid = grid


    def draw(self):
        restValues = str(self.grid.sumHeight)[:4] + ", " +str(self.grid.bumpiness) + ", " + str(self.grid.sumHoles) + ", " + str(self.grid.maxColumn) + ", " +str(self.grid.clearedRow)  + ", " + str(self.grid.biggestWheel) + ", " + str(self.grid.hTransitions) + ", " + str(self.grid.fullSquares)

        self.draw_text( self.grid.heights , [( self.position[0] + self.size*5 ), ( self.position[1] + self.size    )], 9)
        self.draw_text( self.grid.holes , [( self.position[0] + self.size*5 ), ( self.position[1] + self.size + 9)], 9)
        self.draw_text( restValues , [( self.position[0] + self.size*5 ), ( self.position[1] + self.size + 18)], 9)

        pygame.draw.rect(self.screen, get_color(Colors.LIGHT_PURPLE), [ self.position[0], self.position[1] , self.size*GRID_WIDTH, self.size*5 ], 2)			
