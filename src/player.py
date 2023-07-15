# player.py

from config import *

class Player:
    def __init__(self, number):
        # Initialize the player with the given player number
        self.number = number
        self.store = PLAYER_1_STORE if number == 1 else PLAYER_2_STORE  # Store is at index 13 for player 1 and index 6 for player 2

    def choose_house(self, board):
        # Choose a house to sow from
        # For simplicity, just choose the house with the most seeds
        if self.number == 1:
            houses = board.houses[0:6]
        else:
            houses = board.houses[7:13]

        max_seeds = max(houses)
        chosen_house = houses.index(max_seeds)
        
        # Adjust chosen_house index if player_number is 2
        if self.number == 2:
            chosen_house += 7

        return chosen_house
