import numpy as np


class GameGrid(object):

    def __init__(self, rows: int, columns: int):
        self.width = rows
        self.height = columns
        self.grid = np.zeros(shape=(columns, rows))

    def __str__(self):
        return f"{self.grid}"

    def update_grid(self, index_x, index_y, value, ship):
        if not ship.rotated:
            for n in range(value):
                self.grid[index_x][index_y + n] = value
        else:
            for n in range(value):
                self.grid[index_x + n][index_y] = value
        print(self.grid)
        print()

    def check_tile(self, index_x, index_y):
        return self.grid[index_x][index_y] == 0

    def grid_length(self):
        return self.width

    def grid_height(self):
        return self.height

