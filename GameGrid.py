class GameGrid(object):

    def __init__(self, rows: int, columns: int):
        self.width = rows
        self.height = columns
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]


    def __str__(self):
        return f"{self.grid}"

    # Update grid when a ship is placed
    def update_grid(self, index_x, index_y, value, ship):
        """Updates the values of the grid to the ship's length when a ship is placed to match its position"""
        if not ship.rotated:        # When the ship is vertical
            for n in range(value):
                self.grid[index_x][index_y + n] = value
        else:                       # When the ship is horizontal
            for n in range(value):
                self.grid[index_x + n][index_y] = value


    # Check if a tile is empty
    def check_tile(self, index_x, index_y, length, rotated):
        """Checks if the tile is empty"""
        if not rotated:
            for n in range(length):
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
        value = self.grid[index_x][index_y]
        if value != 6 and value != 7:       # If the tile has not been attacked
            if value == 0:                  # If the tile is empty
                value = -1 
                self.grid[index_x][index_y] = 7  # Mark as miss
                print(f"Attack at ({index_x}, {index_y}) was a miss") #DEBUG
                return value
            else:
                self.grid[index_x][index_y] = 6  # Mark as hit
                print(f"Attack at ({index_x}, {index_y}) was a hit") #DEBUG

                return value
        return -1
