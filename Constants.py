import os
import pygame
pygame.init()
# CONSTANTS

# GRID
TILE_WIDTH = 40
TILE_HEIGHT = 40
TILE_TRANSPARENCY = 128
NUM_ROWS = 10
NUM_COL = 10

# TEXT
WHITE_FONT_COLOR = (255, 255, 255)
FONT_SIZE = 20
font = pygame.font.Font(None, FONT_SIZE)    #Font for text rendering

# PAUSE BUTTON
PAUSE_X = 480
PAUSE_Y = 480
PAUSE_WIDTH_HEIGHT = 20
PAUSE_TEXT = "Pause"

# DISPLAY
DISPLAY_WIDTH = 1400
DISPLAY_HEIGHT = 800
DEFAULT_CAPTION = "Battleship"

# COLOR
BLACK_BACKGROUND_COLOR = (0, 0, 0)

# IMAGES
IMAGE_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/images"


