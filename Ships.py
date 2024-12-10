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
        self.hit_count = 0

    def load_ship_image(self):
        """Loads the ship image"""
        return pygame.image.load(self.file_location)

    def check_sunken(self):
        """Checks if the ship is sunk"""
        return self.hit_count == self.length
