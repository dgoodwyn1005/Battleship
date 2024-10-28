import numpy as np


class GameGrid(object):

    def __init__(self, rows: int, columns: int):
        self.width = rows
        self.height = columns
        self.grid = np.zeros(shape=(columns, rows))

    def __str__(self):
        return f"{self.grid}"

    # Update grid when a ship is placed
    def update_grid(self, index_x, index_y, value, ship):
        if not ship.rotated:
            for n in range(value):
                self.grid[index_x][index_y + n] = value
        else:
            for n in range(value):
                self.grid[index_x + n][index_y] = value
        print(self.grid)
        print()

    # Check if a tile is empty
    def check_tile(self, index_x, index_y, length, rotated):
        if not rotated:
            for n in range(length):
                print(self.grid[index_x][index_y + n])
                if self.grid[index_x][index_y + n] != 0:
                    return False
        else:
            for n in range(length):
                if self.grid[index_x + n][index_y] != 0:
                    return False
        return True

    def grid_length(self):
        return self.width

    def grid_height(self):
        return self.height
    
    def attack_tile(self, index_x, index_y):
        # Check if tile was already attacked
        # -1 means already attacked, wether it's a hit or a miss
        if self.grid[index_x][index_y] == -1:  
            return False  # Tile already attacked
        
        # Check if a ship is on the tile
        if self.grid[index_x][index_y] != 0:
            self.grid[index_x][index_y] = -1  # Mark as attacked
            return True  # Hit
        else:
            self.grid[index_x][index_y] = -1  # Mark as miss
            return False  # Miss
