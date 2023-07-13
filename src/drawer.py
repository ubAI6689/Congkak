# game_drawer.py

import pygame

class Drawer:
    
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.capturing = False
        self.pause = False

        # Create a pause button
        self.pause_button_rect = pygame.Rect(10, 70, 100, 50)

        # Create a restart button
        self.restart_button_rect = pygame.Rect(10, 10, 100, 50)

        # Load a cursor image
        self.cursor_image = pygame.image.load('../assets/handcursor.png')
        # Hide the default cursor
        pygame.mouse.set_visible(False)

    def draw(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white

        self.draw_capture_message()
        self.draw_pause_message()
        self.draw_pause_button()
        self.draw_restart_button()
        self.draw_player_turn()

        self.draw_houses()
        self.draw_cursor()

        pygame.display.flip()

    def draw_capture_message(self):
        if self.capturing:
            font = pygame.font.Font(None, 36)
            capture_message = f"Player {self.game.current_player.number} is capturing..."
            text_surface = font.render(capture_message, True, (255, 0, 0))
            self.screen.blit(text_surface, (600,300))

    def draw_pause_message(self):
        if self.pause:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Paused", True, (255, 0, 0))  # Red text
            self.screen.blit(text, (600, 300))  # Adjust position as needed

    def draw_pause_button(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.pause_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Pause", True, (255, 255, 255))
        self.screen.blit(text, self.pause_button_rect)

    def draw_restart_button(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.restart_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, (255, 255, 255))
        self.screen.blit(text, self.restart_button_rect)

    def draw_player_turn(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player {self.game.current_player.number}'s turn", True, (0, 0, 0))
        self.screen.blit(text, (1200, 10))  # Adjust the position as needed

    def draw_houses(self):
        for i, seeds in enumerate(self.game.board.houses):
            if i == 6 or i == 13:  # Stores
                pygame.draw.circle(self.screen, (0, 0, 0), self.game.get_pos_of_house(i), 90)
            else:  # Small holes
                pygame.draw.circle(self.screen, (0, 0, 0), self.game.get_pos_of_house(i), 45)
            # Draw the number of seeds in each house
            font = pygame.font.Font(None, 36)
            text = font.render(str(seeds), True, (255, 255, 255))
            self.screen.blit(text, self.game.get_pos_of_house(i))
            # Draw the index of each house
            index_font = pygame.font.Font(None, 24)
            index_text = index_font.render(str(i), True, (255, 0, 0))  # Red text
            self.screen.blit(index_text, (self.game.get_pos_of_house(i)[0], self.game.get_pos_of_house(i)[1] - 30))  # Draw above the house

    def draw_cursor(self):
        font = pygame.font.Font(None, 36)
        cursor_text = font.render(f"{self.game.seeds_to_move}", True, (0, 0, 0))  # Black text
        cursor_width, cursor_height = self.cursor_image.get_size()

        # Flip the cursor if it's player 2's turn
        if self.game.current_player.number == 2:
            cursor_rect = pygame.Rect(self.game.cursor_pos[0] - cursor_width // 2, self.game.cursor_pos[1] - cursor_height, cursor_width, cursor_height)
            cursor_image_flipped = pygame.transform.flip(self.cursor_image, False, True)
            self.screen.blit(cursor_image_flipped, cursor_rect)
            text_pos = (cursor_rect.center[0], cursor_rect.center[1] - 20)  # Adjust the y-coordinate
        else:
            cursor_rect = self.cursor_image.get_rect(center=(self.game.cursor_pos[0], self.game.cursor_pos[1] + self.cursor_image.get_height() // 2))
            self.screen.blit(self.cursor_image, cursor_rect)
            text_pos = cursor_rect.center
        
        self.screen.blit(cursor_text, text_pos)
