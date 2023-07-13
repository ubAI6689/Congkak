import pygame
from game import CongkakGame
from config import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = CongkakGame(screen)
    game.run()

if __name__ == "__main__":
    main()
