# game_drawer.py

import pygame
from config import *

class Drawer:
    
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        # Create a pause button
        self.pause_button_rect = pygame.Rect(PAUSE_BUTTON_DIM)

        # Create a restart button
        self.restart_button_rect = pygame.Rect(RESTART_BUTTON_DIM)

        # Load a cursor image
        self.cursor_image = pygame.image.load(CURSOR_IMAGE)

        # YES and NO buttons for confirming starting houses
        self.yes_button_rect = pygame.Rect((SCREEN_WIDTH / 2 - 150, 0.13 * SCREEN_HEIGHT + 50, 100, 50))
        self.no_button_rect = pygame.Rect((SCREEN_WIDTH / 2 + 50, 0.13 * SCREEN_HEIGHT + 50, 100, 50))

        # Hide the default cursor
        pygame.mouse.set_visible(True)

    def draw(self):
        self.screen.fill((SCREEN_FILL_COLOR))  # Fill the screen with white

        if self.game.game_state in (self.game.PLAYER_1_SELECTING, self.game.PLAYER_2_SELECTING):
            self.draw_selecting()
            self.draw_start_prompt()
            self.draw_hover_highlight()
        elif self.game.game_state == self.game.CONFIRM_SELECTION:
            self.draw_selecting()
            self.draw_confirmation()

        # Draw houses here
        self.draw_houses()

        if self.game.game_state == self.game.BOTH_PLAYING:
            self.draw_both_playing_cursor()  # Draw two cursors instead of one

        self.draw_player_turn()
        self.draw_restart_button()
        self.draw_pause_message()
        self.draw_pause_button()
        self.draw_capture_message()
        self.draw_winning_message()

        if self.game.game_state != self.game.BOTH_PLAYING:  # Don't draw the cursor again if we're in the BOTH_PLAYING state
            self.draw_cursor()

        pygame.display.flip()

    def draw_selecting(self):
    # Draw a special highlight around the selected starting house
        for player_num in PLAYER_NUMBERS:
            starting_house = self.game.starting_house[player_num-1]
            if starting_house is not None:
                x, y = self.game.get_pos_of_house(starting_house)
                pygame.draw.circle(self.screen, GREEN, (x, y), HOUSE_SIZE + SELECTION_THICKNESS)

    def draw_hover_highlight(self):
        # Draw a special highlight around the hovered house
        hovered_house = self.game.hovered_house
        if hovered_house is not None:
            x, y = self.game.get_pos_of_house(hovered_house)
            color = YELLOW  # The color for a hovered house
            # Check if the hovered house is the selected starting house for the current player
            if self.game.starting_house[self.game.current_player.number - 1] == hovered_house:
                color = GREEN  # The color for a selected starting house
            pygame.draw.circle(self.screen, color, (x, y), HOUSE_SIZE + SELECTION_THICKNESS)


    def draw_start_prompt(self):
        prompt_font = pygame.font.Font(None, 36)
        prompt_color = pygame.Color('black')
        for player_num in PLAYER_NUMBERS:
            if self.game.game_state == self.game.PLAYER_1_SELECTING:
                prompt_text = f"Player 1, please select your starting house."
            elif self.game.game_state == self.game.PLAYER_2_SELECTING:
                prompt_text = f"Player 2, please select your starting house."
            else:
                return  # No prompt text in other game states

            # Create the surface for the prompt text
            prompt_surf = prompt_font.render(prompt_text, True, prompt_color)
            prompt_rect = prompt_surf.get_rect()

            # Position the prompt in the middle of the top of the screen
            prompt_rect.midtop = (SCREEN_WIDTH / 2, 0.1 * SCREEN_HEIGHT)

            # Draw the prompt text on the screen
            self.screen.blit(prompt_surf, prompt_rect)


    def draw_confirmation(self):
        if self.game.game_state == self.game.CONFIRM_SELECTION:
            # Draw the confirmation message
            confirm_font = pygame.font.Font(None, 36)
            confirm_color = pygame.Color('black')
            confirm_text = "START GAME NOW?"
            confirm_surf = confirm_font.render(confirm_text, True, confirm_color)
            confirm_rect = confirm_surf.get_rect()
            confirm_rect.center = (0.5 * SCREEN_WIDTH , 0.1 * SCREEN_HEIGHT)
            self.screen.blit(confirm_surf, confirm_rect)

            # Draw the "Yes" button
            yes_button_rect = pygame.Rect((SCREEN_WIDTH / 2 - 150, 0.13 * SCREEN_HEIGHT + 50, 100, 50))
            pygame.draw.rect(self.screen, PAUSE_BUTTON_COLOR, yes_button_rect)
            yes_font = pygame.font.Font(None, PAUSE_BUTTON_FONT_SIZE)
            yes_text = yes_font.render("Yes", True, WHITE)
            yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
            self.screen.blit(yes_text, yes_text_rect)

            # Draw the "No" button
            no_button_rect = pygame.Rect((SCREEN_WIDTH / 2 + 50, 0.13 * SCREEN_HEIGHT + 50, 100, 50))
            pygame.draw.rect(self.screen, PAUSE_BUTTON_COLOR, no_button_rect)
            no_font = pygame.font.Font(None, PAUSE_BUTTON_FONT_SIZE)
            no_text = no_font.render("No", True, WHITE)
            no_text_rect = no_text.get_rect(center=no_button_rect.center)
            self.screen.blit(no_text, no_text_rect)

    def draw_starting_house_selections(self):
        # Draw a special highlight around the selected starting houses
        for player_num in PLAYER_NUMBERS:
            starting_house = self.game.starting_house[player_num-1]
            if starting_house is not None:
                house, confirmed = starting_house
                x, y = self.game.get_pos_of_house(starting_house)
                # Choose a color based on whether the player has confirmed their selection
                color = YELLOW if confirmed else RED
                pygame.draw.circle(self.screen, color, (x, y), HOUSE_SIZE + SELECTION_THICKNESS)

    def draw_capture_message(self):
        if self.game.animator.capturing:
            font = pygame.font.Font(CAPTURE_FONT, CAPTURE_FONT_SIZE)
            capture_message = f"Player {self.game.current_player.number} is capturing..."
            text_surface = font.render(capture_message, True, (CAPTURE_MSG_COLOR))
            self.screen.blit(text_surface, CAPTURE_MSG_DIM)

    def draw_winning_message(self):
        if self.game.game_over:
            winner = self.game.board.check_winner()
            if winner is not None:
                winning_message = f"Game over. Player {winner} win."
                font = pygame.font.Font(CAPTURE_FONT, CAPTURE_FONT_SIZE)
                text_surface = font.render(winning_message, True, RED)
                self.screen.blit(text_surface, CAPTURE_MSG_DIM)
            else:
                print("Draw method: It's a draw.")
                draw_message = f"It's a draw."
                font = pygame.font.Font(CAPTURE_FONT, CAPTURE_FONT_SIZE)
                text_surface = font.render(draw_message, True, RED)
                self.screen.blit(text_surface, CAPTURE_MSG_DIM)

    def draw_pause_message(self):
        if self.game.pause:
            font = pygame.font.Font(PAUSE_FONT, PAUSE_FONT_SIZE)
            text = font.render("Game Paused", True, PAUSE_MSG_COLOR)  # Red text
            self.screen.blit(text, PAUSE_MSG_DIM)  # Adjust position as needed

    def draw_pause_button(self):
        pygame.draw.rect(self.screen, PAUSE_BUTTON_COLOR, self.pause_button_rect)
        font = pygame.font.Font(PAUSE_BUTTON_FONT, PAUSE_BUTTON_FONT_SIZE)
        text = font.render("Pause", True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.pause_button_rect.center
        self.screen.blit(text, text_rect)

    def draw_restart_button(self):
        pygame.draw.rect(self.screen, RESTART_BUTTON_COLOR, self.restart_button_rect)
        font = pygame.font.Font(RESTART_BUTTON_FONT, RESTART_BUTTON_FONT_SIZE)
        text = font.render("Restart", True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.restart_button_rect.center
        self.screen.blit(text, text_rect)

    def draw_player_turn(self):
        font = pygame.font.Font(TURN_MSG_FONT, TURN_MSG_FONT_SIZE)
        
        if self.game.game_state == self.game.BOTH_PLAYING:
            text = font.render(f"Simultaneous turn", True, TURN_MSG_COLOR)
        else: 
            text = font.render(f"Player {self.game.current_player.number}'s turn", True, TURN_MSG_COLOR)    
        self.screen.blit(text, (0.75 * SCREEN_WIDTH, 10))  # Adjust the position as needed

    def draw_houses(self):
        for i, seeds in enumerate(self.game.board.houses):
            if i in STORE_INDICES:  # Stores
                pygame.draw.circle(self.screen, BLACK, self.game.get_pos_of_house(i), STORE_SIZE)
                font = pygame.font.Font(STORE_SEED_FONT, STORE_SEED_FONT_SIZE)
            else:  # Small houses
                pygame.draw.circle(self.screen, BLACK, self.game.get_pos_of_house(i), HOUSE_SIZE)
                font = pygame.font.Font(SEED_FONT, SEED_FONT_SIZE)

            # Draw the number of seeds in each house
            text = font.render(str(seeds), True, SEED_COLOR)
            self.screen.blit(text, self.game.get_pos_of_house(i))

            # Draw the index of each house
            index_font = pygame.font.Font(HOUSE_INDEX_FONT, HOUSE_INDEX_FONT_SIZE)
            index_text = index_font.render(chr(65 + i), True, HOUSE_INDEX_COLOR)  # Red text
            self.screen.blit(index_text, (self.game.get_pos_of_house(i)[0], self.game.get_pos_of_house(i)[1] - 30))  # Draw above the house

    def draw_cursor(self):
        font = pygame.font.Font(CURSOR_FONT, CURSOR_FONT_SIZE)
        if self.game.current_player.number == 1:
            cursor_pos = self.game.animator.get_cursor_pos_1()
            seeds_to_move = self.game.animator.get_seeds_to_move_1()
        else:
            cursor_pos = self.game.animator.get_cursor_pos_2()
            seeds_to_move = self.game.animator.get_seeds_to_move_2()
        if cursor_pos is None:  # Don't try to draw the cursor if its position is None
            return
        cursor_width, cursor_height = self.cursor_image.get_size()
        # Flip the cursor if it's player 2's turn
        if self.game.current_player.number == 2:
            cursor_rect = pygame.Rect(cursor_pos[0] - cursor_width // 2, cursor_pos[1] - cursor_height, cursor_width, cursor_height)
            cursor_image_flipped = pygame.transform.flip(self.cursor_image, False, True)
            cursor_text = font.render(f"{seeds_to_move}", True, BLUE)  # Black text
            self.screen.blit(cursor_image_flipped, cursor_rect)
            text_pos = (cursor_rect.center[0], cursor_rect.center[1] - 20)  # Adjust the y-coordinate
        else:
            cursor_rect = self.cursor_image.get_rect(center=(cursor_pos[0], cursor_pos[1] + self.cursor_image.get_height() // 2))
            self.screen.blit(self.cursor_image, cursor_rect)
            cursor_text = font.render(f"{seeds_to_move}", True, RED)  # Black text
            text_pos = cursor_rect.center
        self.screen.blit(cursor_text, text_pos)


    def draw_both_playing_cursor(self):
        font = pygame.font.Font(CURSOR_FONT, CURSOR_FONT_SIZE)

        # Draw the cursor for Player 1
        cursor_pos_1 = self.game.animator.get_cursor_pos_1()
        print("From Draw: Cursor 1: " + str(cursor_pos_1))
        
        if cursor_pos_1 is not None:
            seeds_to_move_1 = self.game.animator.get_seeds_to_move_1()
            cursor_text_1 = font.render(f"{seeds_to_move_1}", True, RED)  # Black text
            cursor_rect_1 = self.cursor_image.get_rect(center=(cursor_pos_1[0], cursor_pos_1[1] + self.cursor_image.get_height() // 2))
            self.screen.blit(self.cursor_image, cursor_rect_1)
            self.screen.blit(cursor_text_1, cursor_rect_1.center)

        # Draw the cursor for Player 2
        cursor_pos_2 = self.game.animator.get_cursor_pos_2()
        print("From Draw: Cursor 2: " + str(cursor_pos_2))
        if cursor_pos_2 is not None:
            seeds_to_move_2 = self.game.animator.get_seeds_to_move_2()
            cursor_text_2 = font.render(f"{seeds_to_move_2}", True, BLUE)  # Black text
            cursor_rect_2 = pygame.Rect(cursor_pos_2[0] - self.cursor_image.get_width() // 2, cursor_pos_2[1] - self.cursor_image.get_height(), self.cursor_image.get_width(), self.cursor_image.get_height())
            cursor_image_flipped = pygame.transform.flip(self.cursor_image, False, True)
            self.screen.blit(cursor_image_flipped, cursor_rect_2)
            self.screen.blit(cursor_text_2, (cursor_rect_2.center[0], cursor_rect_2.center[1] - 20))  # Adjust the y-coordinate

