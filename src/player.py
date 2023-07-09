class Player:
    def __init__(self, player_number):
        # Initialize the player with the given player number
        self.player_number = player_number
        self.store = 13 if player_number == 1 else 6  # Store is at index 6 for player 1 and index 13 for player 2

    def choose_house(self, board):
        # Choose a house to sow from
        # For simplicity, just choose the house with the most seeds
        if self.player_number == 1:
            houses = board.houses[0:6]
        else:
            houses = board.houses[7:13]

        max_seeds = max(houses)
        chosen_house = houses.index(max_seeds)
        
        # Adjust chosen_house index if player_number is 2
        if self.player_number == 2:
            chosen_house += 7

        return chosen_house
