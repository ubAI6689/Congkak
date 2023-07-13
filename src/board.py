from config import *

class Board:
    def __init__(self):
        # Initialize the board
        self.houses = BOARD_HOUSES.copy()

    def print_board(self):
        print("Current state of the board:")
        print(" " + " ".join(str(seeds) for seeds in self.houses[PLAYER_2_MIN_HOUSE:PLAYER_2_STORE]))
        print(str(self.houses[PLAYER_1_STORE]) + " " * INIT_SEEDS + " " * 2  + str(self.houses[PLAYER_2_STORE]))
        print(" " + " ".join(str(seeds) for seeds in reversed(self.houses[PLAYER_1_MIN_HOUSE:PLAYER_1_STORE])))

    def is_row_empty(self, player_number):
        if player_number == PLAYER_1:
            print("Checking Player 1 row")
            houses_to_check = self.houses[PLAYER_1_MIN_HOUSE:PLAYER_1_MAX_HOUSE+1]
        elif player_number == PLAYER_2:
            print("Checking Player 2 row")
            houses_to_check = self.houses[PLAYER_2_MIN_HOUSE:PLAYER_2_MAX_HOUSE+1]
        else:
            return False  # Invalid player number

        return all(seeds == 0 for seeds in houses_to_check)

    def is_players_house(self, player_number, house):
        if player_number == PLAYER_1:
            return PLAYER_1_MIN_HOUSE <= house <= PLAYER_1_MAX_HOUSE
        else:  # player_number == PLAYER_2
            return PLAYER_2_MIN_HOUSE <= house <= PLAYER_2_MAX_HOUSE

    def check_game_end(self):
        # Check if all houses are empty
        return all(seeds == 0 for seeds in self.houses[PLAYER_2_MIN_HOUSE:PLAYER_2_MAX_HOUSE+1] + self.houses[PLAYER_1_MIN_HOUSE:PLAYER_1_MAX_HOUSE+1])


    def check_winner(self):
        # Compare the number of seeds in each player's store
        if self.houses[PLAYER_2_STORE] < self.houses[PLAYER_1_STORE]:
            return PLAYER_1  # Player 1 wins
        elif self.houses[PLAYER_2_STORE] > self.houses[PLAYER_1_STORE]:
            return PLAYER_2  # Player 2 wins
        else:
            return None  # It's a draw

    def sow_seeds(self, house, player):
        # Get the number of seeds in the house
        seeds = self.houses[house]
        # Empty the house
        self.houses[house] = 0
        return seeds

        # Handle the last seed
        if house != player.store:
            if self.houses[house] == 1:  # Last seed landed in an empty house
                opposite_house = 12 - house
                if self.houses[opposite_house] > 0:  # Opposite house is not empty
                    # Capture the seeds
                    player.seeds += self.houses[opposite_house] + 1
                    self.houses[house] = 0
                    self.houses[opposite_house] = 0
            elif self.houses[house] > 1:
                self.sow_seeds(house, player)

    
