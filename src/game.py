# game.py

import pygame
import time
from board import Board
from player import Player
from drawer import Drawer
from animator import Animator
from config import *

class CongkakGame:

    PLAYER_1_SELECTING = 0
    PLAYER_2_SELECTING = 1
    CONFIRM_SELECTION = 2
    PLAYING = 3
    ONE_PLAYER_ENDED_CAN_CONTINUE = 4
    ONE_PLAYER_ENDED_WAITING = 5
    TURN_BASED = 6

    def __init__(self, screen):
        
        self.screen = screen
        self.board = Board()
        self.drawer = Drawer(screen, self)
        self.animator = Animator(self)
        self.players = [Player(i) for i in PLAYER_NUMBERS]
        self.current_player = self.players[0]
        self.game_state = self.PLAYER_1_SELECTING
        self.starting_house = [None, None]
        self.hovered_house = None

        self.clock = pygame.time.Clock()  # Pygame clock for limiting framerate
        self.frame_elapsed = 0  # The number of frames elapsed since the last move

        # Pause state
        self.pause = False
        self.game_over = False

    def handle_event(self, event):
        if self.game_state == self.PLAYER_1_SELECTING:
            self.handle_event_player_1_selecting(event)
        elif self.game_state == self.PLAYER_2_SELECTING:
            self.handle_event_player_2_selecting(event)
        elif self.game_state == self.CONFIRM_SELECTION:
            self.handle_event_confirm_selection(event)
        elif self.game_state == self.PLAYING:
            self.handle_event_playing(event)

    def handle_event_player_1_selecting(self, event):
        pos = pygame.mouse.get_pos()
        house = self.get_house_at_pos(pos)
        if house is not None and PLAYER_1_MIN_HOUSE <= house <= PLAYER_1_MAX_HOUSE:
            if event.type == pygame.MOUSEMOTION:
                # Set the hovered house as the player moves the mouse
                self.hovered_house = house
            elif event.type == pygame.MOUSEBUTTONUP:
                # Confirm the selection when the player clicks
                self.starting_house[0] = house
                self.game_state = self.PLAYER_2_SELECTING
                self.change_player()  # Change to player 2 after confirming player 1's selection

    def handle_event_player_2_selecting(self, event):
        pos = pygame.mouse.get_pos()
        house = self.get_house_at_pos(pos)
        if house is not None and PLAYER_2_MIN_HOUSE <= house <= PLAYER_2_MAX_HOUSE:
            if event.type == pygame.MOUSEMOTION:
                # Set the hovered house as the player moves the mouse
                self.hovered_house = house
            elif event.type == pygame.MOUSEBUTTONUP:
                # Confirm the selection when the player clicks
                self.starting_house[1] = house
                self.game_state = self.CONFIRM_SELECTION

    def handle_event_confirm_selection(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            yes_button_rect = pygame.Rect((SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 50, 100, 50))
            no_button_rect = pygame.Rect((SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2 + 50, 100, 50))
            if yes_button_rect.collidepoint(pos):
                self.game_state = self.PLAYING
            elif no_button_rect.collidepoint(pos):
                self.game_state = self.PLAYER_1_SELECTING



    def handle_event_playing(self, event):
        # Your existing game playing event handling logic goes here
        pass

    # def handle_event(self, event):
    #     # Handle a single Pygame event
    #     if event.type == pygame.MOUSEBUTTONUP:
            
    #         pos = pygame.mouse.get_pos()

    #         # Check if the pause button was clicked
    #         if self.drawer.pause_button_rect.collidepoint(pos):
    #             self.toggle_pause()

    #         # Check if the restart button was clicked
    #         if self.drawer.restart_button_rect.collidepoint(pos):
    #             self.restart()
            
    #         if not self.animator.get_animating():
    #             # Check if the mouse clicked on one of the current player's houses
    #             house = self.get_house_at_pos(pos)
    #             if house is not None and house != PLAYER_1_STORE and house != PLAYER_2_STORE:  # make sure stores cannot be clicked
    #                 # get seeds in the house
    #                 seeds = self.board.houses[house]
    #                 if seeds > 0:
    #                     # Check if the house is in the current player's row
    #                     if (self.current_player.number == PLAYER_1 and PLAYER_1_MIN_HOUSE <= house <= PLAYER_1_MAX_HOUSE) or (self.current_player.number == PLAYER_2 and PLAYER_2_MIN_HOUSE <= house <= PLAYER_2_MAX_HOUSE):
    #                         seeds_to_move = self.board.sow_seeds(house, self.current_player)
    #                         self.animator.start_move(house, seeds_to_move)  # start moving seeds from the clicked house

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

        if house in (PLAYER_1_STORE, PLAYER_2_STORE):  # The stores
            if house == PLAYER_1_STORE:
                first_house_x, _ = self.get_pos_of_house(0)
                x = first_house_x - STORE_SIZE - gap  # Position the store to the left of the first house
            else:
                last_house_x, _ = self.get_pos_of_house(PLAYER_2_STORE - 1)
                x = last_house_x + STORE_SIZE + gap  # Position the store to the right of the last house
            y = 0.5 * SCREEN_HEIGHT
        else:  # Non-store houses
            if house < PLAYER_2_STORE:  # Top row
                x = start_pos + total_house_width * house
                y = 0.4 * SCREEN_HEIGHT
            else:  # Bottom row
                x = start_pos + total_house_width * (PLAYER_1_STORE - 1 - house)
                y = 0.6 * SCREEN_HEIGHT

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
