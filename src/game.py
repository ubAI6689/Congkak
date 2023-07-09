import pygame
from board import Board
from player import Player

class CongkakGame:
    def __init__(self, screen):
        self.screen = screen  # Pygame screen for drawing
        self.board = Board()  # The game board
        self.players = [Player(1), Player(2)]  # The two players
        self.current_player = self.players[0]  # The current player

    def handle_event(self, event):
        # Handle a single Pygame event
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # Check if the mouse clicked on one of the current player's houses
            house = self.get_house_at_pos(pos)
            if house is not None:
                self.board.sow_seeds(house, self.current_player)

    def update(self):
        # Update the game state
        # For simplicity, just switch the current player after each turn
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def draw(self):
        # Draw the game state to the screen
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        for i, seeds in enumerate(self.board.houses):
            if i == 14 or i == 15:  # Stores
                pygame.draw.circle(self.screen, (0, 0, 0), self.get_pos_of_house(i), 60)
            else:  # Small holes
                pygame.draw.circle(self.screen, (0, 0, 0), self.get_pos_of_house(i), 30)
            # Draw the number of seeds in each house
            font = pygame.font.Font(None, 24)
            text = font.render(str(seeds), True, (255, 255, 255))
            self.screen.blit(text, self.get_pos_of_house(i))
        pygame.display.flip()

    def run(self):
        # The main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.flip()

    def get_house_at_pos(self, pos):
        # Return the index of the house at the given mouse position, or None if there isn't one
        pass

    def get_pos_of_house(self, house):
        # Return the screen position of the given house
        if house < 7:  # Top row
            x = 200 + house * 100
            y = 100
        elif house < 14:  # Bottom row
            x = 200 + (13 - house) * 100
            y = 200
        else:  # The stores
            x = 100 if house == 14 else 900  # Adjust the x-coordinates for the stores
            y = 150
        return x, y


