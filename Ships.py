import pygame.image
import Constants as C

class Ships(object):

    def __init__(self, ship_name: str, ship_length: int):
        self.name = ship_name
        self.length = ship_length
        self.sunken = False
        self.coordinates = []
        self.file_location = C.IMAGE_FOLDER + "/" + ship_name + ".png"

    def load_ship_image(self):
        return pygame.image.load(self.file_location)
