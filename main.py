import pygame
 
from time     import sleep
from game     import Game 
 
def main():

	game = Game((720,860), "Tetris")
	clock = pygame.time.Clock()

	while game.is_running():
		delta = clock.tick()/1000
		game.process()
		game.update(delta)
		game.draw()
		
if __name__=="__main__":
	main()