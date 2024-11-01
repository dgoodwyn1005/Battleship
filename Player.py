import random
class Player:
    def __init__(self):
        # keep track of coordinates that have already been attacked
        self.attacked_coords = set()


class CPU(Player):
    def __init__(self, board_size):
        
        super().__init__()
        self.board_size = board_size

    # The CPU will make a random move based on available coordinates
    def make_move(self, grid):
        """The CPU picks coordinates to attack randomly"""
        valid_move = False
        while not valid_move:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if (row, col) not in self.attacked_coords:
                valid_move = True
        self.attacked_coords.add((row, col))
        # Call GameGrid's method to attack a tile.
        return grid.attack_tile(row, col), (row, col)
