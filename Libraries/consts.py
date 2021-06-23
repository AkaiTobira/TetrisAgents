SQUARE_SIZE = 21
OFFSET      = 50
GRID_HEIGHT = 22
GRID_WIDTH  = 10
FONT_SIZE   = 19
NUM_OF_EPOCh= 150
ROW_MULTIPLER = 1000000

MAX_NUMBER_PER_GAME_HUM = 100000
MAX_NUMBER_PER_GAME_EVO = 1000
MAX_NUMBER_PER_GAME_PSO = 300000
MAX_NUMBER_PER_GAME_NN  = 300000

NUMBER_OF_SCREENS = 2

RANGE_0_GRID_WIDTH     = range(0, GRID_WIDTH)
RANGE_0_GRID_HEIGHT    = range(0, GRID_HEIGHT)
RANGE_0_GRID_HEIGHT_M1 = range(0, GRID_HEIGHT-1)
RANGE_0_GRID_WIDTH_M1  = range(0, GRID_WIDTH-1)
CELL_GRID_HEIGHT = range(0, 3)
CELL_GRID_WIDTH  = range(0, 4)
CELL_GRID_BOTH   = range(0, 12)
RANGE_1_3        = range(1, 3, 1)
deltaTime = 0



import pygame

from enum import Enum

POINT_DISTANCE = 25

import datetime
DATE_TIME = datetime.datetime.now()
DATE_TIME =  str(DATE_TIME.day) + "-" + str(DATE_TIME.month) + "-" + str(DATE_TIME.year) + "_" + str(DATE_TIME.hour) + str(DATE_TIME.minute) + str(DATE_TIME.second)

import collections
_KeysTuple = collections.namedtuple('AppKeys', 
                        ['ChangeScreen', 'ChangeScreen2', 'ChangeScreen3', "SetTimerInfinity", "SetTimerZero", "SetTimerOne", "SetTimerFastButSeen", "ToggleStatsDraw", "RotateLeft", "RotateRight",   "MoveRight",    "MoveLeft",  "DropDown", "SwichVisibility"])
AppKeys = _KeysTuple(      pygame.K_F1 ,   pygame.K_F2 ,    pygame.K_F3 ,   pygame.K_z ,    pygame.K_p ,   pygame.K_x,  pygame.K_g, pygame.K_s, pygame.K_DOWN,  pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT,   pygame.K_SPACE, pygame.K_q )

class Colors(Enum):
	LIGHT_BLUE   = 1
	LIGHT_PURPLE = 17
	LIGHT_PURPL2 = 9	
	LIGHT_RED    = 8
	LIGHTER_RED  = 10
	RED          = 6
	GREEN        = 5
	YELLOW       = 4
	DARK_YELLOW  = 19
	BLUE         = 7
	BLACK        = 0
	NAVYBLUE	 = 11
	WHITE		 = 12
	BLUE_BAR	 = 13
	KHAKI        = 14
	ORANGERED    = 15
	GOLD         = 99
	GRAY         = 2
	CRIMSON      = 18
	DARK_VIOLET  = 3
	
def get_color( color ):
	if color == Colors.DARK_VIOLET:
		return (148,0,211)
	if color == Colors.GRAY:
		return (128,128,128)
	if color == Colors.CRIMSON:
		return (220,20,60)
	if color == Colors.GOLD:
		return (255,215,0)
	if color == Colors.WHITE:
		return (255,255,255)
	if color == Colors.ORANGERED:
		return (255,69,0)
	if color == Colors.KHAKI:
		return (240,230,140)
	if color == Colors.LIGHT_BLUE:
		return (24,191,158)
	if color == Colors.LIGHT_PURPLE:
		return (159,133,188)
	if color == Colors.LIGHT_RED:
		return (255,21,82)
	if color == Colors.RED:
		return (255,0,0)
	if color == Colors.GREEN:
		return (0,255,0)
	if color == Colors.BLUE:         
		return (0,0,255)
	if color == Colors.BLACK:         
		return (0,0,0)
	if color == Colors.YELLOW:         
		return (255,255,0)	
	if color == Colors.DARK_YELLOW:         
		return (44,53,42)		
	if color == Colors.NAVYBLUE:
		return (20,30,47)	
	if color == Colors.WHITE:
		return (255,255,255)
	if color == Colors.BLUE_BAR:
		return (50,160,255)		
	if color == Colors.LIGHTER_RED:
		return (74,28,55)	
	if color == Colors.LIGHT_PURPL2:
		return (26,34,53)					
