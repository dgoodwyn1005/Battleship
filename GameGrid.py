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
        """Updates the values of the grid to the ship's length when a ship is placed to match its position"""
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
        """Checks if the tile is empty"""
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
        """Attacks a tile and returns the value of the tile"""
        #  0: "None", 1: "destroyer", 2: "submarine", 3: "cruiser", 4: "battleship",
        #           5: "aircraft_carrier", 6: "hit", 7: "miss"
        #  Check if tile was already attacked

        value = self.grid[index_x][index_y]
        if value != 6 and value != 7:       # If the tile has not been attacked
            if value == 0:                  # If the tile is empty
                value = -1
                self.grid[index_x][index_y] = 7  # Mark as miss
                return value
            else:
                self.grid[index_x][index_y] = 6  # Mark as hit
                return value
        else:
            # If the tile has been attacked already
            value = -1
            return value
