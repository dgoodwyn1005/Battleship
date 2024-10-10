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
X_OFFSET = 150
Y_OFFSET = 50

# TEXT
WHITE_FONT_COLOR = (255, 255, 255)
FONT_SIZE = 20
font = pygame.font.Font(None, FONT_SIZE)    #Font for text rendering

# PAUSE BUTTON
PAUSE_X = 760
PAUSE_Y = 560
PAUSE_WIDTH_HEIGHT = 40
PAUSE_TEXT = "Pause"

# DISPLAY
DISPLAY_WIDTH = 1400
DISPLAY_HEIGHT = 800
DEFAULT_CAPTION = "Battleship"

# COLOR
BLACK_BACKGROUND_COLOR = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BLUE = (24, 123, 205)

# IMAGES
IMAGE_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/images"


# OPTIONS SCREEN

# Music button
OPTIONS_CAPTION = "Options"
MUSIC_X = 610
MUSIC_Y = 300
MUSIC_WIDTH = 100
MUSIC_HEIGHT = 60
MUSIC_TEXT = "Toggle Music"

# Sounds button
SOUNDS_X = 715
SOUNDS_Y = 300
SOUNDS_WIDTH = 100
SOUNDS_HEIGHT = 60
SOUNDS_TEXT = "Toggle Sounds"

# Back button
BACK_X = 0
BACK_Y = 0
BACK_WIDTH_HEIGHT = 50
BACK_TEXT = "Back"


