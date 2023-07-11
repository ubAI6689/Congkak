import pygame
import time
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

        self.passed_store = False  # Tracks whether the current move has passed the player's store
        print(f"Passed store is now {self.passed_store}")

        # pause
        self.pause = False

        # Create a pause button
        self.pause_button_rect = pygame.Rect(10, 70, 100, 50)

        # Create a restart button
        self.restart_button_rect = pygame.Rect(10, 10, 100, 50)

    def is_current_players_house(self, house):
        if (self.current_player.number == 1 and 7 <= house < 13) or (self.current_player.number == 2 and 0 <= house < 7):
            return True
        return False
        
    def handle_event(self, event):
        # Handle a single Pygame event
        if event.type == pygame.MOUSEBUTTONUP:
            
            pos = pygame.mouse.get_pos()

            # Check if the pause button was clicked
            if self.pause_button_rect.collidepoint(pos):
                self.toggle_pause()

            # Check if the restart button was clicked
            if self.restart_button_rect.collidepoint(pos):
                self.restart()
            
            if not self.animating:
                # Check if the mouse clicked on one of the current player's houses
                house = self.get_house_at_pos(pos)
                if house is not None and house != 6 and house != 13:  # make sure stores cannot be clicked
                    # get seeds in the house
                    seeds = self.board.houses[house]
                    if seeds > 0:
                        # Check if the house is in the current player's row
                        if (self.current_player.number == 1 and 7 <= house < 13) or (self.current_player.number == 2 and 0 <= house < 6):
                            seeds_to_move = self.board.sow_seeds(house, self.current_player)
                            self.start_move(house, seeds_to_move)  # start moving seeds from the clicked house

    def update(self):
        # Update the game state
        if self.animating and not self.pause:
            if self.cursor_pos != self.target_pos:
                # Move the cursor towards the target
                self.cursor_pos = self.move_towards(self.cursor_pos, self.target_pos, 6.5)  # 10 is the speed of the cursor
            else:
                # Move a seed from the source house to the target house
                self.seeds_to_move -= 1
                self.board.houses[self.target_house] += 1
                if self.target_house == self.current_player.store:
                    self.passed_store = True
                    print(f"Passed store is now {self.passed_store}")

                time.sleep(0.05)  # Pause for 5 millisecond

                # If all seeds have been moved, end the animation
                if self.seeds_to_move == 0:
                    if self.is_store(self.target_house):
                        self.passed_store = False  # Reset passed_store to False at the end of a move
                        self.animating = False
                        print(f"Passed store is now {self.passed_store}")
                        # If the current player's houses are all empty, switch the player
                        if self.current_player.number == 1 and all(seeds == 0 for seeds in self.board.houses[7:13]):
                            self.current_player = self.players[1]
                        elif self.current_player.number == 2 and all(seeds == 0 for seeds in self.board.houses[:6]):
                            self.current_player = self.players[0]

                    # If the target house is non-empty and not a store, continue the movement
                    elif self.board.houses[self.target_house] > 1:
                        seeds_to_drop = self.board.houses[self.target_house]
                        self.board.houses[self.target_house] = 0  # Empty the target house
                        self.seeds_to_move = seeds_to_drop  # Update the remaining seeds to move
                        # Move the cursor to the next house before continuing the movement
                        self.target_house = (self.target_house + 1) % 14
                        # Skip the opponent's store
                        if (self.current_player.number == 1 and self.target_house == 6) or (self.current_player.number == 2 and self.target_house == 13):
                            self.target_house = (self.target_house + 1) % 14
                        self.target_pos = self.get_pos_of_house(self.target_house)
                    else:
                        self.animating = False

                        # Capturing logic
                        if self.passed_store and self.is_current_players_house(self.target_house) and self.board.houses[self.target_house] == 1:
                            print(f"Trying to capture from house {self.target_house}")
                            print(f"Seeds in target house: {self.board.houses[self.target_house]}")
                            print(f"Seeds in opposite house: {self.board.houses[12 - self.target_house]}")

                            # Capture all the seeds in the opposite house
                            opposite_house = 12 - self.target_house
                            captured_seeds = self.board.houses[opposite_house]
                            
                            # if opposite_house is empty, end the move
                            if captured_seeds == 0:
                                self.passed_store = False
                                self.animating = False
                                self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
                                print(f"Passed store is now {self.passed_store}")

                            # animate the capture

                            # Empty the opposite house and the target house
                            self.board.houses[opposite_house] = 0
                            self.board.houses[self.target_house] = 0
                            # Add the captured seeds to the player's store
                            self.board.houses[self.current_player.store] += captured_seeds + 1
                            print(f"Captured {captured_seeds} seeds from house {opposite_house}")
                            print(f"Total of {captured_seeds+1} seeds added to store Player {self.current_player.number}")

                        # Switch the current player after a move has been finished
                        self.passed_store = False  # Reset passed_store to False at the end of a move
                        print(f"Passed store is now {self.passed_store}")

                        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
                # Otherwise, move to the next house
                else:
                    # Calculate the next target house index
                    next_house = (self.target_house + 1) % 14
                    # Skip the opponent's store and check if the movement continues
                    while (self.current_player.number == 1 and next_house == 6) or (self.current_player.number == 2 and next_house == 13):
                        next_house = (next_house + 1) % 14
                    # Update the target house and position
                    self.target_house = next_house
                    if self.target_house == self.current_player.store:
                        self.passed_store = True
                    self.target_pos = self.get_pos_of_house(self.target_house)

        else:
            if not self.pause:
                # # When the animation ends, move the cursor to the start of the current player's houses
                # if self.current_player.number == 1:
                #     x, y = self.cursor_pos = self.get_pos_of_house(7)  # The first house of player 1
                #     self.cursor_pos = (x, y + 50)  # Move the cursor down by 50 pixels
                # else:
                #     x, y = self.cursor_pos = self.get_pos_of_house(0)  # The first house of player 2
                #     self.cursor_pos = (x, y - 50)  # Move the cursor up by 50 pixels

                # Update the cursor position to follow the mouse
                self.cursor_pos = pygame.mouse.get_pos()

        # After updating the game state, check if the game is over
        if self.check_game_end():
            winner = self.check_winner()
            if winner is None:
                print("The game is a draw.")
            else:
                print(f"Player {winner.number} wins.")

    def check_game_end(self):
        # Check if all houses are empty
        if all(seeds == 0 for seeds in self.board.houses[:6] + self.board.houses[7:13]):
            # If so, the game is over
            return True
        return False

    def check_winner(self):
        # Compare the number of seeds in each player's store
        if self.board.houses[6] < self.board.houses[13]:
            return self.players[0]  # Player 1 wins
        elif self.board.houses[6] > self.board.houses[13]:
            return self.players[1]  # Player 2 wins
        else:
            return None  # It's a draw

    def is_store(self, house):
        if (self.current_player.number == 1 and house == 13) or (self.current_player.number == 2 and house == 6):
            return True
        return False

    def draw(self):
        # Draw the game state to the screen
        self.screen.fill((255, 255, 255))  # Fill the screen with white

        if self.pause:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Paused", True, (255, 0, 0))  # Red text
            self.screen.blit(text, (600, 300))  # Adjust position as needed

        # Draw the pause button
        pygame.draw.rect(self.screen, (0, 0, 0), self.pause_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Pause", True, (255, 255, 255))
        self.screen.blit(text, self.pause_button_rect)

        # Draw the restart button
        pygame.draw.rect(self.screen, (0, 0, 0), self.restart_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (255, 255, 255))
        self.screen.blit(text, self.restart_button_rect)

        # Draw the player turn
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player {self.current_player.number}'s turn", True, (0, 0, 0))
        self.screen.blit(text, (1200, 10))  # Adjust the position as needed

        for i, seeds in enumerate(self.board.houses):
            if i == 6 or i == 13:  # Stores
                pygame.draw.circle(self.screen, (0, 0, 0), self.get_pos_of_house(i), 90)
            else:  # Small holes
                pygame.draw.circle(self.screen, (0, 0, 0), self.get_pos_of_house(i), 45)
            # Draw the number of seeds in each house
            font = pygame.font.Font(None, 36)
            text = font.render(str(seeds), True, (255, 255, 255))
            self.screen.blit(text, self.get_pos_of_house(i))
            # Draw the index of each house
            index_font = pygame.font.Font(None, 24)
            index_text = index_font.render(str(i), True, (255, 0, 0))  # Red text
            self.screen.blit(index_text, (self.get_pos_of_house(i)[0], self.get_pos_of_house(i)[1] - 30))  # Draw above the house
        
        # Draw the cursor with the number of seeds to move
        cursor_text = font.render(f"{self.seeds_to_move}", True, (0, 0, 0))  # Black text
        cursor_width, cursor_height = self.cursor_image.get_size()

        # Flip the cursor if it's player 2's turn
        if self.current_player.number == 2:
            cursor_rect = pygame.Rect(self.cursor_pos[0] - cursor_width // 2, self.cursor_pos[1] - cursor_height, cursor_width, cursor_height)
            cursor_image_flipped = pygame.transform.flip(self.cursor_image, False, True)
            self.screen.blit(cursor_image_flipped, cursor_rect)
            text_pos = (cursor_rect.center[0], cursor_rect.center[1] - 20)  # Adjust the y-coordinate
        else:
            cursor_rect = self.cursor_image.get_rect(center=(self.cursor_pos[0], self.cursor_pos[1] + self.cursor_image.get_height() // 2))
            self.screen.blit(self.cursor_image, cursor_rect)
            text_pos = cursor_rect.center
        
        self.screen.blit(cursor_text, text_pos)
        pygame.display.flip()

    # Add a new method to start a move animation
    def start_move(self, source_house, seeds_to_move):
        self.animating = True
        self.source_house = source_house
        self.target_house = (source_house + 1) % 14
        self.seeds_to_move = seeds_to_move
        self.cursor_pos = self.get_pos_of_house(source_house)
        self.target_pos = self.get_pos_of_house((source_house + 1) % 14)

        # Switch the current player after a move has been started
        # self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

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
        if house < 6:  # Top row
            x = 380 + house * 150  # Multiply x-coordinates by 1.5
            y = 200  # Multiply y-coordinates by 2
        elif house < 13 and house > 6:  # Bottom row
            x = 380 + (12 - house) * 150  # Multiply x-coordinates by 1.5
            y = 400  # Multiply y-coordinates by 2
        else:  # The stores
            x = 200 if house == 13 else 1300  # Multiply x-coordinates by 1.5
            y = 300  # Multiply y-coordinates by 2
        return x, y
    
    def toggle_pause(self):
        self.pause = not self.pause

    def restart(self):
        # Reset the game state
        self.board = Board()  # Create a new board
        self.current_player = self.players[0]  # Set the current player to player 1
        self.animating = False  # Reset the animation state
        self.source_house = None  # Reset the source house
        self.target_house = None  # Reset the target house
        self.seeds_to_move = 0  # Reset the seeds to move
        self.cursor_pos = (0, 0)  # Reset the cursor position
        self.target_pos = None  # Reset the target cursor position
        self.passed_store = False  # Reset the passed store flag
        self.pause = False  # Unpause the game if it was paused

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

