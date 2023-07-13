from config import *

class Board:
    def __init__(self):
        # Initialize the board
        self.houses = BOARD_HOUSES.copy()

    def is_row_empty(self, player_number):
        if player_number == PLAYER_1:
            houses_to_check = self.houses[PLAYER_1_MIN_HOUSE:PLAYER_1_MAX_HOUSE]
        elif player_number == PLAYER_2:
            houses_to_check = self.houses[PLAYER_2_MIN_HOUSE:PLAYER_2_MAX_HOUSE]
        else:
            return False  # Invalid player number

        return all(seeds == 0 for seeds in houses_to_check)

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
