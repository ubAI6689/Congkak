import pygame
from game import CongkakGame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1500, 600))
    game = CongkakGame(screen)
    game.run()

if __name__ == "__main__":
    main()
