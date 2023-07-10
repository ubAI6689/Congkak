class Board:
    def __init__(self):
        # Initialize the board with 7 seeds in each house and 0 in each store
        self.houses = [6] * 6 + [0] + [6] * 6 + [0]  # 7 seeds in each house, 0 in each store

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
