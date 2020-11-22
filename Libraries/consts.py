SQUARE_SIZE = 37
OFFSET      = 50
GRID_HEIGHT = 22
GRID_WIDTH  = 10
FONT_SIZE   = 26
NUM_OF_EPOCh= 150
ROW_MULTIPLER = 1000000
MAX_NUMBER_PER_GAME = 5000
import pygame

from enum import Enum

POINT_DISTANCE = 25

import datetime
DATE_TIME = datetime.datetime.now()
DATE_TIME = str(DATE_TIME.year) + str(DATE_TIME.month) + str(DATE_TIME.day) + "_" + str(DATE_TIME.hour) + str(DATE_TIME.minute) + str(DATE_TIME.second)

class AppKeys(Enum):
	ChangeScreen = pygame.K_F1,

import collections
_KeysTuple = collections.namedtuple('AppKeys', 
                        ['ChangeScreen', "SetTimerInfinity", "SetTimerZero", "SetTimerOne", "RotateLeft", "RotateRight",   "MoveRight",    "MoveLeft",  "DropDown", "SwichVisibility"])
AppKeys = _KeysTuple(      pygame.K_F1 ,        pygame.K_z ,    pygame.K_p ,   pygame.K_x, pygame.K_DOWN,  pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT,   pygame.K_SPACE, pygame.K_q )

class Colors(Enum):
	LIGHT_BLUE   = 1
	LIGHT_PURPLE = 2
	LIGHT_PURPL2 = 3	
	LIGHT_RED    = 4
	LIGHTER_RED  = 5
	RED          = 6
	GREEN        = 7
	YELLOW       = 8
	DARK_YELLOW  = 9
	BLUE         = 10
	BLACK        = 0
	NAVYBLUE	 = 11
	WHITE		 = 12
	BLUE_BAR	 = 13
	KHAKI        = 14
	ORANGERED    = 15
	GOLD         = 16
	GRAY         = 17
	CRIMSON      = 18
	DARK_VIOLET  = 19
	
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
