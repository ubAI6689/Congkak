class Board:
    def __init__(self):
        # Initialize the board with 7 seeds in each house and 0 in each store
        self.houses = [7] * 14 + [0, 0]

    def sow_seeds(self, house, player):
        # Perform the sowing operation from the given house
        seeds = self.houses[house]
        self.houses[house] = 0

        while seeds > 0:
            house = (house + 1) % 14  # Move to the next house
            if house == player.store:  # Skip the opponent's store
                continue
            self.houses[house] += 1
            seeds -= 1

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
