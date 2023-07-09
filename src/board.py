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
        if house != player.store and self.houses[house] > 1:
            self.sow_seeds(house, player)
