import numpy as np

class gamegrid(object):

    def __init__(self, rows:int, columns:int):
        self.width = rows
        self.height = columns
        self.grid = np.zeros(shape=(rows, columns))

    def __str__(self):
        return f"{self.grid}"

    def configure_grid(self, index_x, index_y, value):
        self.grid[index_x][index_y] = value

    def grid_length(self):
        return self.width
    
    def grid_height(self):
        return self.height