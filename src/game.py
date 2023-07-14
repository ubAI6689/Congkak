# game.py

import pygame
import time
from board import Board
from player import Player
from drawer import Drawer
from animator import Animator
from config import *

class CongkakGame:
    def __init__(self, screen):
        self.screen = screen  # Pygame screen for drawing
        self.board = Board()  # The game board
        self.drawer = Drawer(screen, self) # The game drawer
        self.animator = Animator(self) # The game animator
        self.players = [Player(i) for i in PLAYER_NUMBERS]  # The two players
        self.current_player = self.players[0]  # The current player

        self.clock = pygame.time.Clock()  # Pygame clock for limiting the framerate
        self.frames_elapsed = 0  # Count the number of frames elapsed

        # Pause state
        self.pause = False
        self.game_over = False

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
            
            if not self.animator.get_animating():
                # Check if the mouse clicked on one of the current player's houses
                house = self.get_house_at_pos(pos)
                if house is not None and house != PLAYER_1_STORE and house != PLAYER_2_STORE:  # make sure stores cannot be clicked
                    # get seeds in the house
                    seeds = self.board.houses[house]
                    if seeds > 0:
                        # Check if the house is in the current player's row
                        if (self.current_player.number == PLAYER_1 and PLAYER_1_MIN_HOUSE <= house <= PLAYER_1_MAX_HOUSE) or (self.current_player.number == PLAYER_2 and PLAYER_2_MIN_HOUSE <= house <= PLAYER_2_MAX_HOUSE):
                            seeds_to_move = self.board.sow_seeds(house, self.current_player)
                            self.animator.start_move(house, seeds_to_move)  # start moving seeds from the clicked house

    def update(self):
        if self.game_over:
            return
        if self.animator.get_capturing():
            self.animator.update_capture_state()
        elif self.animator.get_animating() and not self.pause:
            self.animator.animate_seeds_movement()
        else:
            if not self.pause:
                self.animator.set_cursor_pos(pygame.mouse.get_pos())

    def end_move(self):
        # End the current player's move
        self.animator.set_capturing(False)
        self.animator.set_animating(False)  # End the animation
        self.animator.set_passed_store(False)  # Reset the passed_store flag
        self.change_player()  # Change the current player
        print(f"Move end. Player {self.current_player.number}'s turn.")
        print(f"Passed store is now {self.animator.get_passed_store()}")

        # If the current player has no seeds in their houses, end their turn immediately
        if self.board.is_row_empty(self.current_player.number):
            print(f"Player {self.current_player.number} has no seeds in their houses. Changing turn ...")
            self.change_player()
            print(f"Player {self.current_player.number}'s turn.")
            self.board.print_board()

        # Every time the move end, check if the game is over
        if not self.animator.get_animating() and self.board.check_game_end():
            winner = self.board.check_winner()
            if winner is None:
                print("The game is a draw.")
            else:
                print(f"Player {winner} wins.")
            self.game_over = True

    def change_player(self):
        ## Change the current player
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def run(self):
        # The main game loop
        running = True
        while running:
            self.clock.tick(FPS_LIMIT)  # Limit the framerate to 60 FPS
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
        for i in range(MAX_HOUSE_COUNT):
            house_x, house_y = self.get_pos_of_house(i)
            if abs(x - house_x) <= 45 and abs(y - house_y) <= 45:  # Within 45 pixels of the center of the house
                return i
        return None

    def get_pos_of_house(self, house):
        # Return the screen position of the given house
        gap_ratio = 0.3 
        gap = SCREEN_WIDTH * gap_ratio // (INIT_HOUSE_ROW - 1)
        total_house_width = HOUSE_SIZE + gap
        total_row_width = total_house_width * INIT_HOUSE_ROW - 1.5 * gap
        start_pos = 0.5 * SCREEN_WIDTH - total_row_width / 2

        if house < PLAYER_2_STORE:  # Top row
            x = start_pos + total_house_width * house
            y = 0.4 * SCREEN_HEIGHT
        elif house < PLAYER_1_STORE and house > PLAYER_2_STORE:  # Bottom row
            x = start_pos + total_house_width * (PLAYER_1_STORE - 1 - house)
            y = 0.6 * SCREEN_HEIGHT
        else:  # The stores
            if house == PLAYER_1_STORE:
                first_house_x, _ = self.get_pos_of_house(0)
                x = first_house_x - STORE_SIZE - gap  # Position the store to the left of the first house
            else:
                last_house_x, _ = self.get_pos_of_house(PLAYER_2_STORE - 1)
                x = last_house_x + STORE_SIZE + gap  # Position the store to the right of the last house
            y = 0.5 * SCREEN_HEIGHT
        return x, y
    
    def toggle_pause(self):
        self.pause = not self.pause

    def restart(self):
        # Reset the game state
        print(f"Restarting...")
        self.animator.set_animating(False) # Reset the animation state
        self.board = Board()  # Create a new board
        self.current_player = self.players[0]  # Set the current player to player 1
        self.animator.set_source_house(None)
        self.animator.set_target_house(None)  # Reset the target house
        self.animator.set_seeds_to_move(0)  # Reset the seeds to move
        # self.cursor_pos = (0, 0)  # Reset the cursor position
        self.animator.set_target_pos(None)  # Reset the target cursor position
        self.animator.set_passed_store(False)  # Reset the passed store flag
        self.pause = False  # Unpause the game if it was paused
        self.game_over = False  # Reset the game over flag
