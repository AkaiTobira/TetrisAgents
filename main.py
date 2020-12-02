import pygame
import threading

from time           import sleep
from Libraries.game_master import GameMaster
from Libraries.Structures.best_saver import *

 
def main():
	pygame.init()
	game = GameMaster()
	clock = pygame.time.Clock()

	#drawThread = threading.Thread(target=game.process)
	#drawThread.daemon = True
	#drawThread.start()
	#drawThread.run()

	while game.is_running():
		delta = clock.tick()/1000
		game.process()
		game.update(delta)
		game.draw()

	#drawThread.join()
		
if __name__=="__main__":
	main()