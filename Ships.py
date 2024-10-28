import pygame.image
import Constants as C

class Ships(object):

    def __init__(self, ship_name: str, ship_length: int):
        self.name = ship_name
        self.length = ship_length
        self.sunken = False
        self.file_location = C.IMAGE_FOLDER + "/" + ship_name + ".png"
        self.head_coordinate = (-1, -1)
        self.rotated = False
    # add a method to load the ship image? Maybe?
    # add a coordinate for the ship to replace them on the grid with their orientation
    # Add a count for the number of hits on the ship

    def load_ship_image(self):
        return pygame.image.load(self.file_location)


