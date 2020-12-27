import pygame
import threading

from time           import sleep
from Libraries.game_master import GameMaster
from Libraries.Structures.best_saver import *
from Libraries.consts import deltaTime
from Libraries.Structures.meansures import Time

def main():
	pygame.init()
	game = GameMaster()

	while game.is_running():
		Time.update()
		game.process()
		game.update(Time.delta)
		game.draw()

if __name__=="__main__":
	main()