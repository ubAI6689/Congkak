# animator.py

from config import *
import time

class Animator:
    def __init__(self, game):
        self.game = game
        self.animating = False
        self.source_house = None
        self.target_house = None
        self.seeds_to_move = 0
        self.cursor_pos = None
        self.target_pos = None
        self.passed_store = False
        self.capturing = False
        self.capture_phase = 0

    # Getter methods
    def get_animating(self):
        return self.animating

    def get_source_house(self):
        return self.source_house

    def get_target_house(self):
        return self.target_house

    def get_seeds_to_move(self):
        return self.seeds_to_move

    def get_cursor_pos(self):
        return self.cursor_pos

    def get_target_pos(self):
        return self.target_pos
    
    def get_passed_store(self):
        return self.passed_store
    
    def get_capturing(self):
        return self.capturing
    
    def get_capture_phase(self):
        return self.capture_phase

    # Setter methods
    def set_animating(self, animating):
        self.animating = animating

    def set_source_house(self, source_house):
        self.source_house = source_house

    def set_target_house(self, target_house):
        self.target_house = target_house

    def set_seeds_to_move(self, seeds_to_move):
        self.seeds_to_move = seeds_to_move

    def set_cursor_pos(self, cursor_pos):
        self.cursor_pos = cursor_pos

    def set_target_pos(self, target_pos):
        self.target_pos = target_pos
    
    def set_passed_store(self, passed_store):
        self.passed_store = passed_store
    
    def set_capturing(self, capturing):
        self.capturing = capturing
    
    def set_capture_phase(self, capture_phase):
        self.capture_phase = capture_phase

    def start_move(self, source_house, seeds_to_move):
        self.set_animating(True)
        self.set_source_house(source_house)
        self.set_target_house((source_house + 1) % MAX_HOUSE_COUNT)
        self.set_seeds_to_move(seeds_to_move)
        self.set_cursor_pos(self.game.get_pos_of_house(source_house))
        self.set_target_pos(self.game.get_pos_of_house((source_house + 1) % MAX_HOUSE_COUNT))
        print(f"Player {self.game.current_player.number} move from house no {source_house} towards house no {(source_house + seeds_to_move) % MAX_HOUSE_COUNT}.")

    def animate_seeds_movement(self):
        # Move the cursor towards the target position
        self.set_cursor_pos(self.move_towards(self.get_cursor_pos(), self.get_target_pos(), ANIMATION_SPEED))

        # If the cursor has reached the target position
        if self.get_cursor_pos() == self.get_target_pos():
            # Move a seed from the source house to the target house
            self.set_seeds_to_move(self.get_seeds_to_move() - 1)
            print(f"Seeds to move: {self.get_seeds_to_move()}")
            self.game.board.houses[self.get_target_house()] += 1
            if self.get_target_house() == self.game.current_player.store:
                self.set_passed_store(True)
                print(f"Passed store is now {self.get_passed_store()}")

            time.sleep(SLEEP_TIME)  # Pause for 5 millisecond

            # If all seeds have been moved, check if the movement continues or not
            if self.get_seeds_to_move() == 0:
                self.handle_end_of_movement()
            else:
                # Calculate the next target house index
                next_house = (self.get_target_house() + 1) % MAX_HOUSE_COUNT
                # Skip the opponent's store and check if the movement continues
                while (self.game.current_player.number == PLAYER_1 and next_house == PLAYER_2_STORE) or (self.game.current_player.number == PLAYER_2 and next_house == PLAYER_1_STORE):
                    next_house = (next_house + 1) % MAX_HOUSE_COUNT
                # Update the target house and position
                self.set_target_house(next_house)
                if self.get_target_house() == self.game.current_player.store:
                    self.set_passed_store(True)
                self.set_target_pos(self.game.get_pos_of_house(self.get_target_house()))


    def move_towards(self, pos, target, speed):
        # Move the position pos towards the target position at the given speed
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        dist = max(abs(dx), abs(dy))
        if dist <= speed:
            return target
        else:
            return (pos[0] + dx / dist * speed, pos[1] + dy / dist * speed)

    def handle_end_of_movement(self):
        # If the target house is the current player's store, the player gets another turn
        if self.get_target_house() == self.game.current_player.store:
            self.set_passed_store(False)  # Reset passed_store to False at the end of a move
            self.set_animating(False) # Reset animating to False at the end of a move
            print(f"Passed store is now {self.get_passed_store()}")
            print(f"Move ends in store. Player {self.game.current_player.number} gets another turn.")
            # If the current player's houses are all empty, end the move
            if self.game.board.is_row_empty(self.game.current_player.number):
                self.game.end_move()

        # If the target house is non-empty and not a store, continue the movement
        elif self.game.board.houses[self.get_target_house()] > 1:
            seeds_to_drop = self.game.board.houses[self.get_target_house()]
            print(f"Move continues to house {(self.get_target_house() + 1 + seeds_to_drop) % MAX_HOUSE_COUNT}.")
            self.game.board.houses[self.get_target_house()] = 0  # Empty the target house
            self.set_seeds_to_move(seeds_to_drop)  # Update the remaining seeds to move
            # Move the cursor to the next house before continuing the movement
            self.set_target_house((self.get_target_house() + 1) % MAX_HOUSE_COUNT)
            # Skip the opponent's store
            if (self.game.current_player.number == PLAYER_1 and self.get_target_house() == PLAYER_2_STORE) or (self.game.current_player.number == PLAYER_2 and self.get_target_house() == PLAYER_1_STORE):
                self.set_target_house((self.get_target_house + 1) % MAX_HOUSE_COUNT)
            self.set_target_pos(self.game.get_pos_of_house(self.get_target_house()))

        # If the target house is empty, check for a capture
        else:
            self.handle_capture_state()

    def update_capture_state(self):
        # Updates the state of the game while a capture is happening
        if self.get_cursor_pos() != self.get_target_pos():
            self.set_cursor_pos(self.move_towards(self.get_cursor_pos(), self.get_target_pos(), ANIMATION_SPEED))
        else:
            if self.get_capture_phase() == CAPTURE_PHASES[0]:
                self.game.board.houses[self.get_target_house()] = 0
                time.sleep(SLEEP_TIME)
                self.set_capture_phase(CAPTURE_PHASES[1])
                self.set_source_house(self.get_target_house)
                self.set_target_house(self.game.current_player.store)
                self.set_target_pos(self.game.get_pos_of_house(self.game.current_player.store))
            elif self.get_capture_phase() == CAPTURE_PHASES[1]:
                self.set_seeds_to_move(self.get_seeds_to_move() - 1)
                self.game.board.houses[self.game.current_player.store] += 1   
                if self.get_seeds_to_move() == 0:
                    self.set_capturing(False)
                    self.set_capture_phase(CAPTURE_PHASES[0])
                    self.game.end_move()
        return

    def handle_capture_state(self):
        # Checks if a capture should happen and initiates it if conditions are met
        if not self.game.board.is_players_house(self.game.current_player.number, self.get_target_house()):
            self.game.end_move()
            return

        if not self.get_passed_store():
            self.game.end_move()
            return

        opposite_house = TOTAL_HOUSE - self.get_target_house()
        captured_seeds = self.game.board.houses[opposite_house]

        if captured_seeds == 0:
            self.game.end_move()
            return

        self.set_capturing(True)
        self.set_capture_phase(CAPTURE_PHASES[0])
        print(f"Trying to capture from house {self.get_target_house()}")
        print(f"Seeds in target house: {self.game.board.houses[self.get_target_house()]}")
        print(f"Seeds in opposite house: {self.game.board.houses[TOTAL_HOUSE - self.get_target_house()]}")
        self.game.board.houses[self.get_target_house()] = 0
        self.set_seeds_to_move(captured_seeds + 1)
        self.set_source_house(self.get_target_house())
        self.set_target_house(opposite_house)
        self.set_target_pos(self.game.get_pos_of_house(opposite_house))
        return
