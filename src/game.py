import pygame
from board import Board
from player import Player

class CongkakGame:
    def __init__(self, screen):
        self.screen = screen  # Pygame screen for drawing
        self.board = Board()  # The game board
        self.players = [Player(1), Player(2)]  # The two players
        self.current_player = self.players[0]  # The current player

        self.clock = pygame.time.Clock()  # Pygame clock for limiting the framerate
        self.frames_elapsed = 0  # Count the number of frames elapsed

        # Load a cursor image
        self.cursor_image = pygame.image.load('../assets/handcursor.png')
        # Hide the default cursor
        pygame.mouse.set_visible(False)

        self.animating = False  # Whether an animation is in progress
        self.source_house = None  # The house seeds are being moved from
        self.target_house = None  # The house seeds are being moved to
        self.seeds_to_move = 0  # The number of seeds left to move

        self.cursor_pos = (0, 0)  # The current cursor position
        self.target_pos = None  # The target cursor position

        self.restart_button_rect = pygame.Rect(10, 10, 100, 50)
        
    def handle_event(self, event):
        # Handle a single Pygame event
        if event.type == pygame.MOUSEBUTTONUP and not self.animating:
            pos = pygame.mouse.get_pos()
            
            # Check if the restart button was clicked
            if self.restart_button_rect.collidepoint(pos):
                self.restart()
            # Check if the mouse clicked on one of the current player's houses
            house = self.get_house_at_pos(pos)
            if house is not None and house != 14 and house != 15:  # make sure stores cannot be clicked
                self.start_move(house, self.board.houses[house])  # start moving seeds from the clicked house


    def update(self):
        # Update the game state
        # For simplicity, just switch the current player after each turn
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

        if self.animating:
            if self.cursor_pos != self.target_pos:
                # Move the cursor towards the target
                self.cursor_pos = self.move_towards(self.cursor_pos, self.target_pos, 10)  # 10 is the speed of the cursor
            else:
                self.frames_elapsed += 1  # Increment the frames elapsed
                if self.frames_elapsed >= 18:  # If 18 frames have elapsed
                    self.frames_elapsed = 0  # Reset the counter
                    # Move a seed from the source house to the target house
                    self.board.houses[self.source_house] -= 1
                    self.board.houses[self.target_house] += 1
                    self.seeds_to_move -= 1
                    # If all seeds have been moved, end the animation
                    if self.seeds_to_move == 0:
                        # If the last house (other than a store) is not empty, continue sowing
                        if self.target_house < 14 and self.board.houses[self.target_house] > 0:
                            self.seeds_to_move = self.board.houses[self.target_house]
                            self.board.houses[self.target_house] = 0
                        else:
                            self.animating = False
                    # Otherwise, move to the next house
                    else:
                        # Calculate the next target house
                        next_target_house = (self.target_house + 1) % 16  # Include the stores

                        # Skip the opponent's store
                        if self.current_player.number == 1 and next_target_house == 15:
                            next_target_house = 0  # Skip to the first house
                        elif self.current_player.number == 2 and next_target_house == 7:
                            next_target_house = 8  # Skip to the next house after the store

                        self.target_house = next_target_house
                        self.target_pos = self.get_pos_of_house(self.target_house)

    def draw(self):
        # Draw the game state to the screen
        self.screen.fill((255, 255, 255))  # Fill the screen with white

        # Draw the restart button
        pygame.draw.rect(self.screen, (0, 0, 0), self.restart_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (255, 255, 255))
        self.screen.blit(text, self.restart_button_rect)

        for i, seeds in enumerate(self.board.houses):
            if i == 14 or i == 15:  # Stores
                pygame.draw.circle(self.screen, (0, 0, 0), self.get_pos_of_house(i), 90)
            else:  # Small holes
                pygame.draw.circle(self.screen, (0, 0, 0), self.get_pos_of_house(i), 45)
            # Draw the number of seeds in each house
            font = pygame.font.Font(None, 36)
            text = font.render(str(max(seeds, 0)), True, (255, 255, 255))
            self.screen.blit(text, self.get_pos_of_house(i))
        
        # Draw the cursor
        self.screen.blit(self.cursor_image, pygame.mouse.get_pos())

        # Draw the cursor at its current position
        self.screen.blit(self.cursor_image, self.cursor_pos)
        
        pygame.display.flip()

    # Add a new method to start a move animation
    def start_move(self, source_house, seeds_to_move):
        self.animating = True
        self.source_house = source_house
        self.target_house = (source_house + 1) % 14
        self.seeds_to_move = seeds_to_move
        self.cursor_pos = self.get_pos_of_house(source_house)
        self.target_pos = self.get_pos_of_house((source_house + 1) % 14)

    @staticmethod
    def move_towards(pos, target, speed):
        # Move the position pos towards the target position at the given speed
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        dist = max(abs(dx), abs(dy))
        if dist <= speed:
            return target
        else:
            return (pos[0] + dx / dist * speed, pos[1] + dy / dist * speed)

    def run(self):
        # The main game loop
        running = True
        while running:
            self.clock.tick(60)  # Limit the framerate to 60 FPS
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
        x, y = pos
        for i in range(16):
            house_x, house_y = self.get_pos_of_house(i)
            if abs(x - house_x) <= 45 and abs(y - house_y) <= 45:  # Within 45 pixels of the center of the house
                return i
        return None

    def get_pos_of_house(self, house):
        # Return the screen position of the given house
        if house < 7:  # Top row
            x = 300 + house * 150  # Multiply x-coordinates by 1.5
            y = 200  # Multiply y-coordinates by 2
        elif house < 14:  # Bottom row
            x = 300 + (13 - house) * 150  # Multiply x-coordinates by 1.5
            y = 400  # Multiply y-coordinates by 2
        else:  # The stores
            x = 120 if house == 14 else 1380  # Multiply x-coordinates by 1.5
            y = 300  # Multiply y-coordinates by 2
        return x, y
    
    def restart(self):
        # Reset the game state
        self.board = Board()  # Create a new board
        self.current_player = self.players[0]  # Set the current player to player 1



