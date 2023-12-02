# game.py

import pygame
import time
import math
from board import Board
from player import Player
from drawer import Drawer
from animator import Animator
from config import *

class CongkakGame:

    PLAYER_1_SELECTING = 0
    PLAYER_2_SELECTING = 1
    CONFIRM_SELECTION = 2
    BOTH_PLAYING = 3
    PAUSE_FOR_NEXT_MOVE = 4
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

        # Compute the x values.
        self.leftmost_house_x = self.get_pos_of_house(PLAYER_1_MAX_HOUSE)[0]
        self.rightmost_house_x = self.get_pos_of_house(PLAYER_1_MIN_HOUSE)[0]

        # Pause state
        self.pause = False
        self.game_over = False


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            if self.drawer.restart_button_rect.collidepoint(pos):
                self.restart()

            # Check if the pause button was clicked
            if self.drawer.pause_button_rect.collidepoint(pos):
                self.toggle_pause()

        if self.game_state == self.PLAYER_1_SELECTING:
            self.handle_event_player_1_selecting(event)
        elif self.game_state == self.PLAYER_2_SELECTING:
            self.handle_event_player_2_selecting(event)
        elif self.game_state == self.CONFIRM_SELECTION:
            self.handle_event_confirm_selection(event)
        # elif self.game_state == self.BOTH_PLAYING:
        #     self.handle_event_both_playing(event)
        # elif self.game_state == self.ONE_PLAYER_ENDED_CAN_CONTINUE:
        #     self.handle_event_one_player_ended_can_continue(event)
        elif self.game_state == self.ONE_PLAYER_ENDED_WAITING:
            self.handle_event_one_player_ended_waiting(event)
        elif self.game_state == self.TURN_BASED:
            self.handle_event_turn_based(event)

    def handle_event_player_1_selecting(self, event):
        pos = self.animator.get_cursor_pos_1()
        if pos is None:
            return  # Ignore events if the cursor position is None
        x, y = pos
        house = self.get_house_at_pos(pos)
        if house is not None and PLAYER_1_MIN_HOUSE <= house <= PLAYER_1_MAX_HOUSE:
            if event.type == pygame.MOUSEMOTION:
                # Ignore movements outside the player's houses
                if self.leftmost_house_x <= pos[0] <= self.rightmost_house_x:
                    # Set the hovered house as the player moves the mouse
                    self.hovered_house = house
            elif event.type == pygame.MOUSEBUTTONUP:
                # Player 2 still has seeds to move, don't change the current player
                if self.animator.get_seeds_to_move_2() > 0:
                    self.starting_house[0] = house
                    self.animator.start_move(self.starting_house[0], self.board.houses[self.starting_house[0]])
                else:
                    # Confirm the selection when the player clicks
                    self.starting_house[0] = house
                    print("Player 1's starting house: ", self.starting_house[0]) 
                    self.animator.set_cursor_pos_1(self.get_pos_of_house(house))  # Set the cursor position to the selected house
                    self.current_player = self.players[1]  # Change to player 2 after confirming player 1's selection
                    self.game_state = self.PLAYER_2_SELECTING

    def handle_event_player_2_selecting(self, event):
        pos = self.animator.get_cursor_pos_2()
        if pos is None:
            return  # Ignore events if the cursor position is None
        x, y = pos
        house = self.get_house_at_pos(pos)
        if house is not None and PLAYER_2_MIN_HOUSE <= house <= PLAYER_2_MAX_HOUSE:
            if event.type == pygame.MOUSEMOTION:
                # Ignore movements outside the player's houses
                if self.leftmost_house_x <= pos[0] <= self.rightmost_house_x:
                    # Set the hovered house as the player moves the mouse
                    self.hovered_house = house
            elif event.type == pygame.MOUSEBUTTONUP:
                # Player 1 still has seeds to move, don't change the current player
                if self.animator.get_seeds_to_move_1() > 0:
                    self.starting_house[1] = house
                    self.animator.start_move(self.starting_house[1], self.board.houses[self.starting_house[1]])
                else:
                    # Confirm the selection when the player clicks
                    self.starting_house[1] = house
                    print("Player 2's starting house: ", self.starting_house[1]) 
                    self.animator.set_cursor_pos_2(self.get_pos_of_house(house))  # Set the cursor position to the selected house
                    self.current_player = self.players[0]  # Change back to player 1
                    self.game_state = self.CONFIRM_SELECTION

    def handle_event_confirm_selection(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.drawer.yes_button_rect.collidepoint(pos):
                self.game_state = self.BOTH_PLAYING
                # Get the seeds from the starting houses
                seeds_to_move_1 = self.board.sow_seeds(self.starting_house[0], self.players[0])
                seeds_to_move_2 = self.board.sow_seeds(self.starting_house[1], self.players[1])
                # Initiate the move for both players
                self.animator.start_move(self.starting_house[0], seeds_to_move_1, self.starting_house[1], seeds_to_move_2)
            elif self.drawer.no_button_rect.collidepoint(pos):
                # reset house to None
                self.starting_house[0] = None
                self.starting_house[1] = None
                self.hovered_house = None
                self.game_state = self.PLAYER_1_SELECTING

    def handle_event_pause_for_next_move(self, event):
        # Check which player(s) ended up in their store
        if self.animator.get_target_house_1() == PLAYER_1_STORE and self.animator.get_target_house_2() == PLAYER_2_STORE:
            self.handle_event_player_1_selecting(event)
            self.handle_event_player_2_selecting(event)
        elif self.animator.get_target_house_1() == PLAYER_1_STORE:
            self.handle_event_player_1_selecting(event)
        elif self.animator.get_target_house_2() == PLAYER_2_STORE:
            self.handle_event_player_2_selecting(event)

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

    # def update(self):
    #     if self.game_over:
    #         return
    #     if self.animator.get_capturing():
    #         self.animator.update_capture_state()
    #     elif self.animator.get_animating() and not self.pause:
    #         self.animator.animate_seeds_movement()
    #     else:
    #         if not self.pause:
    #             mouse_x, mouse_y = pygame.mouse.get_pos()
    #             if self.current_player.leftmost_house_x <= mouse_x <= self.current_player.rightmost_house_x:
    #                 if self.current_player.number == PLAYER_1:
    #                     mouse_y = 0.4 * SCREEN_HEIGHT
    #                 else:  # PLAYER_2
    #                     mouse_y = 0.6 * SCREEN_HEIGHT
    #                 self.animator.set_cursor_pos((mouse_x, mouse_y))

    def update(self):
        if self.game_over:
            return
        if self.animator.get_capturing():
            self.animator.update_capture_state()
        elif self.animator.get_animating() and not self.pause:
            self.animator.animate_movement()
        else:
            if not self.pause:
                pos = pygame.mouse.get_pos()
                if self.game_state in (self.PLAYER_1_SELECTING, self.PLAYER_2_SELECTING):
                    pos = self.get_corrected_cursor_pos(pos)
                    if self.current_player.number == 1:
                        self.animator.set_cursor_pos_1(pos)
                    else:
                        self.animator.set_cursor_pos_2(pos)
                elif self.game_state == self.CONFIRM_SELECTION:
                    self.animator.set_cursor_pos_1(pos)
                    self.animator.set_cursor_pos_2(pos)
                elif self.game_state == self.BOTH_PLAYING:
                    if self.current_player.number == 1:
                        self.animator.set_cursor_pos_1(self.get_pos_of_house(self.starting_house[0]))
                    else:
                        self.animator.set_cursor_pos_2(self.get_pos_of_house(self.starting_house[1]))


    def get_corrected_cursor_pos(self, pos):
        # Get the x limits for the current player's row
        x_min = self.leftmost_house_x
        x_max = self.rightmost_house_x

        # Determine the y coordinate based on the current player.
        if self.current_player.number == 1:
            y = BOTTOM_ROW_Y  # Replace with the y coordinate of player 1's row.
        else:
            y = TOP_ROW_Y  # Replace with the y coordinate of player 2's row.

        # Limit the x coordinate within the player's row
        x = max(min(pos[0], x_max), x_min)

        return (x, y)

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
            if abs(x - house_x) <= HOUSE_CENTER and abs(y - house_y) <= HOUSE_CENTER:  # Within 45 pixels of the center of the house
                return i
        return None

    def get_pos_of_house(self, house):
        # Return the screen position of the given house
        gap = GAP
        store_gap = math.sqrt(abs(gap**2 - (gap / 2)**2)) # to make sure the distance travelled by cursors are consistent
        total_house_width = HOUSE_SIZE + gap
        total_row_width = total_house_width * INIT_HOUSE_ROW - 1.5 * gap
        start_pos = 0.5 * SCREEN_WIDTH - total_row_width / 2

        if house in (PLAYER_1_STORE, PLAYER_2_STORE):  # The stores
            if house == PLAYER_1_STORE:
                first_house_x, _ = self.get_pos_of_house(0)
                x = first_house_x - STORE_SIZE - store_gap  # Position the store to the left of the first house
            else:
                last_house_x, _ = self.get_pos_of_house(PLAYER_2_STORE - 1)
                x = last_house_x + STORE_SIZE + store_gap  # Position the store to the right of the last house
            y = CENTER_ROW
        else:  # Non-store houses
            if house < PLAYER_2_STORE:  # Top row
                x = start_pos + total_house_width * house
                y = TOP_ROW_Y
            else:  # Bottom row
                x = start_pos + total_house_width * (PLAYER_1_STORE - 1 - house)
                y = BOTTOM_ROW_Y

        return x, y
    
    def get_opponent(self, player):
        # Assuming you have two players, player1 and player2
        if player == self.players[0]:
            return self.players[1]
        else:
            return self.players[0]
        
    def add_seed_to_house(self, house_index):
        self.board.houses[house_index] += 1

    def empty_house(self, house_index):
        self.board.houses[house_index] = 0

    def add_seed_to_store(self, player_number):
        if player_number == 1:
            self.board.houses[PLAYER_1_STORE] += 1
        else:
            self.board.houses[PLAYER_2_STORE] += 1
    
    def toggle_pause(self):
        print(f"Pause: {self.pause}")
        self.pause = not self.pause

    def restart(self):
        # Reset the game state
        print(f"Restarting...")
        self.starting_house[0] = None
        self.starting_house[1] = None
        self.hovered_house = None
        self.current_player = self.players[0]
        self.game_state = self.PLAYER_1_SELECTING

        self.animator.set_animating(False) # Reset the animation state
        self.board = Board()  # Create a new board
        self.animator.set_source_house_1(None)
        self.animator.set_source_house_2(None)
        self.animator.set_target_house_1(None)  # Reset the target house
        self.animator.set_target_house_2(None)  # Reset the target house
        self.animator.set_seeds_to_move_1(0)  # Reset the seeds to move
        self.animator.set_seeds_to_move_2(0)  # Reset the seeds to move
        
        self.animator.set_target_pos_1(None)  
        self.animator.set_target_pos_2(None)  
        self.animator.set_passed_store_1(False)  # Reset the passed store flag
        self.animator.set_passed_store_2(False)  # Reset the passed store flag
        self.pause = False  # Unpause the game if it was paused
        self.game_over = False  # Reset the game over flag
