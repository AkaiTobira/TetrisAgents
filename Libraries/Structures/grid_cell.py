import pygame

from Libraries.consts import *

class GridCell:
    screen = None
    rect   = None
    color  = get_color(Colors.KHAKI)
    fill   = get_color(Colors.BLACK)

    m_id   = 0
    def __init__(self, screen, center):
        self.m_id        = int((center[0] - OFFSET)/SQUARE_SIZE * GRID_HEIGHT + (center[1] - OFFSET)/SQUARE_SIZE)
        self.rect        = pygame.Rect(  SQUARE_SIZE/2, SQUARE_SIZE/2, SQUARE_SIZE,   SQUARE_SIZE )
        self.screen      = screen
        self.rect.center = center

    def draw(self):
        pygame.draw.rect(self.screen, self.fill , self.rect    )
        pygame.draw.rect(self.screen, self.color, self.rect, 1 )

    def fill_cell(self, color):
        self.fill = color

