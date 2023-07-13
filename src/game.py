import pygame
import time
from board import Board
from player import Player
from drawer import Drawer

class CongkakGame:
    def __init__(self, screen):
        self.screen = screen  # Pygame screen for drawing
        self.board = Board()  # The game board
        self.drawer = Drawer(screen, self) # The game drawer
        self.players = [Player(1), Player(2)]  # The two players
        self.current_player = self.players[0]  # The current player

        self.clock = pygame.time.Clock()  # Pygame clock for limiting the framerate
        self.frames_elapsed = 0  # Count the number of frames elapsed

        self.animating = False  # Whether an animation is in progress
        self.source_house = None  # The house seeds are being moved from
        self.target_house = None  # The house seeds are being moved to
        self.seeds_to_move = 0  # The number of seeds left to move

        self.cursor_pos = (0, 0)  # The current cursor position
        self.target_pos = None  # The target cursor position

        self.passed_store = False  # Tracks whether the current move has passed the player's store
        print(f"Passed store is now {self.passed_store}")

        self.capturing = False  # Tracks whether a capture is in progress
        self.capture_phase = 0  # Tracks the current phase of the capture

        # pause
        self.pause = False

    def is_current_players_house(self, house):
        if (self.current_player.number == 1 and 7 <= house < 13) or (self.current_player.number == 2 and 0 <= house < 7):
            return True
        return False
        
    def handle_event(self, event):
        # Handle a single Pygame event
        if event.type == pygame.MOUSEBUTTONUP:
            
            pos = pygame.mouse.get_pos()

            # Check if the pause button was clicked
            if self.drawer.pause_button_rect.collidepoint(pos):
                self.toggle_pause()

            # Check if the restart button was clicked
            if self.drawer.restart_button_rect.collidepoint(pos):
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
        # Check if a capture is in progress
        if self.capturing:
            # Execute the capture movement code
            if self.cursor_pos != self.target_pos:
                self.cursor_pos = self.move_towards(self.cursor_pos, self.target_pos, 6.5)
            else:
                # First phase of capture: move from current house to opposite house
                if self.capture_phase == 1:
                    self.board.houses[self.target_house] = 0
                    time.sleep(0.08)
                    # Start the second phase: move from opposite house to store
                    self.capture_phase = 2
                    self.source_house = self.target_house
                    self.target_house = self.current_player.store
                    self.target_pos = self.get_pos_of_house(self.current_player.store)
                # Second phase of capture: move from opposite house to store
                    print(f"Total captured seeds: {self.seeds_to_move}")
                elif self.capture_phase == 2:
                    self.seeds_to_move -= 1
                    self.board.houses[self.current_player.store] += 1   
                    if self.seeds_to_move == 0:
                        # End the capture
                        self.capturing = False
                        self.capture_phase = 0
                        self.end_move()
            return  # Skip the rest of the update method

        # Update the game state
        if self.animating and not self.pause:
            if self.cursor_pos != self.target_pos:
                # Move the cursor towards the target
                self.cursor_pos = self.move_towards(self.cursor_pos, self.target_pos, 8)  # 10 is the speed of the cursor
            else:
                # Move a seed from the source house to the target house
                self.seeds_to_move -= 1
                print(f"Seeds to move: {self.seeds_to_move}")
                self.board.houses[self.target_house] += 1
                if self.target_house == self.current_player.store:
                    self.passed_store = True
                    print(f"Passed store is now {self.passed_store}")

                time.sleep(0.08)  # Pause for 5 millisecond

                # If all seeds have been moved, check if the movement continues or not
                if self.seeds_to_move == 0:

                    # If the target house is the current player's store, the player gets another turn
                    if self.target_house == self.current_player.store:
                        self.passed_store = False  # Reset passed_store to False at the end of a move
                        self.animating = False
                        print(f"Passed store is now {self.passed_store}")
                        print(f"Move ends in store. Player {self.current_player.number} gets another turn.")
                        # If the current player's houses are all empty, end the move
                        if self.current_player.number == 1 and all(seeds == 0 for seeds in self.board.houses[7:13]):
                            self.end_move()
                        elif self.current_player.number == 2 and all(seeds == 0 for seeds in self.board.houses[:6]):
                            self.end_move()

                    # If the target house is non-empty and not a store, continue the movement
                    elif self.board.houses[self.target_house] > 1:
                        seeds_to_drop = self.board.houses[self.target_house]
                        print(f"Move continues to house {(self.target_house + 1 + seeds_to_drop) % 14}.")
                        self.board.houses[self.target_house] = 0  # Empty the target house
                        self.seeds_to_move = seeds_to_drop  # Update the remaining seeds to move
                        # Move the cursor to the next house before continuing the movement
                        self.target_house = (self.target_house + 1) % 14
                        # Skip the opponent's store
                        if (self.current_player.number == 1 and self.target_house == 6) or (self.current_player.number == 2 and self.target_house == 13):
                            self.target_house = (self.target_house + 1) % 14
                        self.target_pos = self.get_pos_of_house(self.target_house)

                    # If the target house is empty, check for a capture
                    else:
                        # if not own house, end the move
                        if not self.is_current_players_house(self.target_house):
                            self.end_move()
                            return

                        # if own house, but has not passed store, end the move
                        if self.passed_store == False:
                            self.end_move()
                            return

                        # if own house and has passed store, check the seeds in the opposite house
                        opposite_house = 12 - self.target_house
                        captured_seeds = self.board.houses[opposite_house]

                        # if no seeds to be captured, end the move
                        if captured_seeds == 0:
                            self.end_move()
                            return

                        # if there are seeds to be captured, start the capture
                        self.capturing = True
                        self.capture_phase = 1
                        print(f"Trying to capture from house {self.target_house}")
                        print(f"Seeds in target house: {self.board.houses[self.target_house]}")
                        print(f"Seeds in opposite house: {self.board.houses[12 - self.target_house]}")
                        # Empty the opposite house and the target house
                        self.board.houses[self.target_house] = 0
                        # Set the seeds_to_move to the number of captured seeds plus one (the seed in the current house)
                        self.seeds_to_move = captured_seeds + 1
                        # Start the animation from the current house to the opposite house
                        self.source_house = self.target_house
                        self.target_house = opposite_house
                        self.target_pos = self.get_pos_of_house(opposite_house)
                        return  # Return from the update method to allow the main game loop to continue

                # Otherwise (if seeds to move is not yet 0), move to the next house
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
                self.cursor_pos = pygame.mouse.get_pos()

        # After updating the game state, check if the game is over
        if self.check_game_end():
            winner = self.check_winner()
            if winner is None:
                print("The game is a draw.")
            else:
                print(f"Player {winner.number} wins.")

    def end_move(self):
        # End the current player's move
        self.capturing = False
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
        self.animating = False  # End the animation
        # reset the passed_store flag
        self.passed_store = False
        print(f"Move end. Player {self.current_player.number}'s turn.")
        print(f"Passed store is now {self.passed_store}")

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

    # Add a new method to start a move animation
    def start_move(self, source_house, seeds_to_move):
        self.animating = True
        self.source_house = source_house
        self.target_house = (source_house + 1) % 14
        self.seeds_to_move = seeds_to_move
        self.cursor_pos = self.get_pos_of_house(source_house)
        self.target_pos = self.get_pos_of_house((source_house + 1) % 14)
        print(f"Player {self.current_player.number} move from house no {source_house} towards house no {(source_house + seeds_to_move) % 14}.")

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
            self.drawer.draw()
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

