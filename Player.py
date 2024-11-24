import random
class Player(object):
    def __init__(self):
        # keep track of coordinates that have already been attacked
        self.attacked_coords = set()


class CPU(Player):
    def __init__(self, board_size):
        
        super().__init__()
        self.board_size = board_size
        
        # Store adjacent tiles for targeting
        self.targeting_queue = [(3,3)]

        #Track last successful hit
        #self.last_hit = None

    # The CPU will make a random move based on available coordinates
    def make_move(self, grid):
        """The CPU picks coordinates to attack randomly at first, and the CPU will target adjacent tiles
        if a hit is successful."""
        print(f"Starting make_move. Targeting queue length: {len(self.targeting_queue)}") #DEBUG
        # If last hit is succesful, use the targeting queue
        if self.targeting_queue:
            print(f"Targeting queue: {self.targeting_queue}") #DEBUG
            row, col = self.targeting_queue.pop(0)
            print(f"Targeting tile: ({row}, {col})") #DEBUG
            if (row, col) not in self.attacked_coords:
                self.attacked_coords.add((row, col))
                result = grid.attack_tile(row, col)
                print(f"Result of targetted attack: {result}") #DEBUG

                #if it's a hit
                if result != -1:
                    print(f"Hit at ({row}, {col})! Adding adjacent tiles.") #DEBUG
                    self.add_adjacent_tiles(row, col)
                return result, (row, col)
        
        # If last hit is NOT successful, make a random move
        print("CPU falling back to random move") #DEBUG
        valid_move = False
        while not valid_move:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if (row, col) not in self.attacked_coords:
                valid_move = True
            elif len(self.attacked_coords) == self.board_size ** 2:  # If all coordinates have been attacked for testing
                return None, None
        self.attacked_coords.add((row, col))
        # Call GameGrid's method to attack a tile.
        return grid.attack_tile(row, col), (row, col)

    def add_adjacent_tiles(self, row, col):
        """Add tiles adjacent to a hit to the targeting queue"""
        # Add above, below, left, and right to targeting queue
        potential_targets = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        print(f"Adding adjacent tiles for a hit at ({row}, {col}): {potential_targets}") #DEBUG

        for r, c in potential_targets:
            if 0 <= r < self.board_size and 0 <= c < self.board_size and (r, c) not in self.attacked_coords:
                self.targeting_queue.append((r, c))
        print(f"Updated targeting queue: {self.targeting_queue}") #DEBUG
