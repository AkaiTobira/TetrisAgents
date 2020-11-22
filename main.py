import pygame
 
from time           import sleep
from Libraries.game_master import GameMaster
 
def main():
	pygame.init()
	game = GameMaster()
	clock = pygame.time.Clock()

	while game.is_running():
		delta = clock.tick()/1000
		game.process()
		game.update(delta)
		game.draw()
		
if __name__=="__main__":
	main()