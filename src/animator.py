from config import *
import time
import math

class Animator:
    def __init__(self, game):
        self.game = game
        self.animating = False
        self.capturing = False
        self.capture_phase = 0
        
        # Initialize Player 1 variables
        self.source_house_1 = None
        self.target_house_1 = None
        self.seeds_to_move_1 = 0
        self.cursor_pos_1 = None
        self.target_pos_1 = None
        self.passed_store_1 = False

        # Initialize Player 2 variables
        self.source_house_2 = None
        self.target_house_2 = None
        self.seeds_to_move_2 = 0
        self.cursor_pos_2 = None
        self.target_pos_2 = None
        self.passed_store_2 = False

    # Getter methods for animator flags
    def get_animating(self):
        return self.animating
    def get_capturing(self):
        return self.capturing
    def get_capture_phase(self):
        return self.capture_phase

    # Getter methods for Player 1
    def get_source_house_1(self):
        return self.source_house_1
    def get_target_house_1(self):
        return self.target_house_1
    def get_seeds_to_move_1(self):
        return self.seeds_to_move_1
    def get_cursor_pos_1(self):
        return self.cursor_pos_1
    def get_target_pos_1(self):
        return self.target_pos_1
    def get_passed_store_1(self):
        return self.passed_store_1
    
    # Getter methods for Player 2
    def get_source_house_2(self):
        return self.source_house_2
    def get_target_house_2(self):
        return self.target_house_2
    def get_seeds_to_move_2(self):
        return self.seeds_to_move_2
    def get_cursor_pos_2(self):
        return self.cursor_pos_2
    def get_target_pos_2(self):
        return self.target_pos_2
    def get_passed_store_2(self):
        return self.passed_store_2

    # Setter methods for animator flags
    def set_animating(self, animating):
        self.animating = animating
    def set_capturing(self, capturing):
        self.capturing = capturing
    def set_capture_phase(self, capture_phase):
        self.capture_phase = capture_phase

    # Setter methods for Player 1
    def set_source_house_1(self, source_house_1):
        self.source_house_1 = source_house_1
    def set_target_house_1(self, target_house_1):
        self.target_house_1 = target_house_1
    def set_seeds_to_move_1(self, seeds_to_move_1):
        self.seeds_to_move_1 = seeds_to_move_1
    def set_cursor_pos_1(self, cursor_pos_1):
        self.cursor_pos_1 = cursor_pos_1
    def set_target_pos_1(self, target_pos_1):
        self.target_pos_1 = target_pos_1
    def set_passed_store_1(self, passed_store_1):
        self.passed_store_1 = passed_store_1

    # Setter methods for Player 2
    def set_source_house_2(self, source_house_2):
        self.source_house_2 = source_house_2
    def set_target_house_2(self, target_house_2):
        self.target_house_2 = target_house_2
    def set_seeds_to_move_2(self, seeds_to_move_2):
        self.seeds_to_move_2 = seeds_to_move_2
    def set_cursor_pos_2(self, cursor_pos_2):
        self.cursor_pos_2 = cursor_pos_2
    def set_target_pos_2(self, target_pos_2):
        self.target_pos_2 = target_pos_2
    def set_passed_store_2(self, passed_store_2):
        self.passed_store_2 = passed_store_2

    # Animation methods
    def start_move(self, source_house_1, seeds_to_move_1, source_house_2, seeds_to_move_2):
        print("Starting move...")
        print("<start_move> Source house for Player 1: ", source_house_1)
        print("<start_move> Source house for Player 2: ", source_house_2)
        self.set_animating(True)
        # Player 1
        self.set_source_house_1(source_house_1)
        self.set_target_house_1((source_house_1 + 1) % MAX_HOUSE_COUNT)
        self.set_seeds_to_move_1(seeds_to_move_1)
        self.set_cursor_pos_1(self.game.get_pos_of_house(source_house_1))
        print("<start_move> Cursor pos for Player 1: ", self.get_cursor_pos_1())
        self.set_target_pos_1(self.game.get_pos_of_house((source_house_1 + 1) % MAX_HOUSE_COUNT))
        # Player 2
        self.set_source_house_2(source_house_2)
        self.set_target_house_2((source_house_2 + 1) % MAX_HOUSE_COUNT)
        self.set_seeds_to_move_2(seeds_to_move_2)
        self.set_cursor_pos_2(self.game.get_pos_of_house(source_house_2))
        print("<start_move> Cursor pos for Player 2: ", self.get_cursor_pos_2())
        # self.set_animating(False) # TODO: Remove this line
        self.set_target_pos_2(self.game.get_pos_of_house((source_house_2 + 1) % MAX_HOUSE_COUNT))

    def animate_movement(self):
        if self.game.game_state == self.game.BOTH_PLAYING:
            self.animate_seeds_movement(2)
            self.animate_seeds_movement(1)
        elif self.game.current_player.number == 1:
            self.animate_seeds_movement(1)
        else:
            self.animate_seeds_movement(2)


    def animate_seeds_movement(self, player_number):
        if player_number == 1:
            cursor_pos = self.get_cursor_pos_1()
            target_pos = self.get_target_pos_1()
            target_house = self.get_target_house_1()
            seeds_to_move = self.get_seeds_to_move_1()
            set_cursor_pos = self.set_cursor_pos_1
            set_seeds_to_move = self.set_seeds_to_move_1
            set_target_house = self.set_target_house_1
            set_target_pos = self.set_target_pos_1
            get_passed_store = self.get_passed_store_1
            set_passed_store = self.set_passed_store_1
        elif player_number == 2:
            cursor_pos = self.get_cursor_pos_2()
            target_pos = self.get_target_pos_2()
            target_house = self.get_target_house_2()
            seeds_to_move = self.get_seeds_to_move_2()
            set_cursor_pos = self.set_cursor_pos_2
            set_seeds_to_move = self.set_seeds_to_move_2
            set_target_house = self.set_target_house_2
            set_target_pos = self.set_target_pos_2
            get_passed_store = self.get_passed_store_2
            set_passed_store = self.set_passed_store_2
        else:
            return

        # Move the cursor towards the target position
        set_cursor_pos(self.move_towards(cursor_pos, target_pos, ANIMATION_SPEED))

        # If the cursor has reached the target position
        if cursor_pos == target_pos:
            time.sleep(SLEEP_TIME)  # Pause for 5 millisecond
            self.game.board.houses[target_house] += 1
            # Move a seed from the source house to the target house
            set_seeds_to_move(seeds_to_move - 1)
            print(f"Seeds to move: {seeds_to_move}")
            if target_house == self.game.current_player.store:
                set_passed_store(True)
                print(f"Passed store is now {get_passed_store()}")

            # If all seeds have been moved, check if the movement continues or not
            if seeds_to_move == 0:
                self.handle_end_of_movement()
            else:
                # Calculate the next target house index
                next_house = (target_house + 1) % MAX_HOUSE_COUNT
                # Skip the opponent's store and check if the movement continues
                # Skip the opponent's store
                # Skip the opponent's store
                while (player_number == PLAYER_1 and next_house == PLAYER_2_STORE) or (player_number == PLAYER_2 and next_house == PLAYER_1_STORE):
                    next_house = (next_house + 1) % MAX_HOUSE_COUNT

                # Update the target house and position
                set_target_house(next_house)
                if (player_number == PLAYER_1 and target_house == PLAYER_1_STORE) or (player_number == PLAYER_2 and target_house == PLAYER_2_STORE):
                    set_passed_store(True)
                    print(f"Player {player_number} passed store is now {get_passed_store()}")
                set_target_pos(self.game.get_pos_of_house(target_house))

    def handle_end_of_movement(self):
        # If the target house is the current player's store, the player gets another turn
        # We need to check for both players now
        if self.get_target_house_1() == self.game.current_player.store and self.get_target_house_2() == self.game.current_player.store:
            self.set_passed_store_1(False)  # Reset passed_store to False at the end of a move
            self.set_passed_store_2(False)  # Reset passed_store to False at the end of a move
            self.set_animating(False)  # Reset animating to False at the end of a move
            print(f"Move ends in store. Player {self.game.current_player.number} gets another turn.")
            # If the current player's houses are all empty, end the move
            if self.game.board.is_row_empty(self.game.current_player.number):
                self.game.end_move()
        else:
            # If the target house is not the current player's store, switch the current player
            pass
    
    # def move_towards(self, pos, target, base_speed):
    #     # Move the position pos towards the target position at a speed proportional to the distance
    #     dx = target[0] - pos[0]
    #     dy = target[1] - pos[1]
    #     dist = math.sqrt(dx**2 + dy**2)
    #     speed = base_speed * dist / MAX_DISTANCE
    #     if dist <= speed:
    #         return target
    #     else:
    #         return (pos[0] + dx / dist * speed, pos[1] + dy / dist * speed)


    def move_towards(self, pos, target, speed):
        # Move the position pos towards the target position at the given speed
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        dist = max(abs(dx), abs(dy))
        print("dx: ", dx, " dy: ", dy, " dist: ", dist)
        if dist <= speed:
            return target
        else:
            return (pos[0] + dx / dist * speed, pos[1] + dy / dist * speed)


    def handle_player_end_of_movement(self):
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
