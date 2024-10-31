import os
import pygame
pygame.init()
# CONSTANTS

# IMAGES Folder
IMAGE_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/images"

# FONTS Folder
FONTS_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/fonts"

# GRID
TILE_WIDTH = 40
TILE_HEIGHT = 40
TILE_TRANSPARENCY = 128
NUM_ROWS = 10
NUM_COL = 10
X_OFFSET = 55
Y_OFFSET = 75
GAME_FONT = pygame.font.Font(FONTS_FOLDER + "/ka1.ttf", 20)
OPPONENT_X_OFFSET = 900
OPPONENT_Y_OFFSET = 80

# TEXT
WHITE_FONT_COLOR = (255, 255, 255)
FONT_SIZE = 20
font = pygame.font.Font(None, FONT_SIZE)    #Font for text rendering

# PAUSE BUTTON
PAUSE_X = 760
PAUSE_Y = 560
PAUSE_WIDTH_HEIGHT = 40
PAUSE_TEXT = "Pause"

# ROTATE BUTTON
ROTATE_X = 710
ROTATE_Y = 100
ROTATE_WIDTH_HEIGHT = 40
ROTATE_TEXT = "Rotate"

# SHIP PREVIEW
SHIP_PREVIEW_X = 600
SHIP_PREVIEW_Y = 200

# DISPLAY
DISPLAY_WIDTH = 1400
DISPLAY_HEIGHT = 800
DEFAULT_CAPTION = "Battleship"

# COLOR
BLACK_BACKGROUND_COLOR = (0, 0, 0)
LIGHTER_BLUE_COLOR = (100, 170, 210)
RED = (255, 0, 0)
GREY = (128, 128, 128)
HOVER_COLOR = (150, 150, 150)
BLUE = (24, 123, 205)
LIGHT_GREY = (101, 100, 100)
DARK_GREEN = (105, 135, 165)
HOVER_COLOR = (150, 150, 150)

# MAIN MENU SCREEN
MENU_CAPTION = "Main Menu"
MENU_TEXT = "Battleship!!!"

INPUT_X = 100  
INPUT_Y = 400  
INPUT_WIDTH = 300  
INPUT_HEIGHT = 50  

# Text
MENU_FONT_SIZE = 200
MENU_FONT = pygame.font.Font(None, MENU_FONT_SIZE)
TEXT_X = 700
TEXT_Y = 100

# Start button
START_X = 600
START_Y = 300
START_WIDTH = 200
START_HEIGHT = 50
START_TEXT = "Start"

# Options button
OPTIONS_X = 600
OPTIONS_Y = 400
OPTIONS_WIDTH = 200
OPTIONS_HEIGHT = 50
OPTIONS_TEXT = "Options"

# Quit button
QUIT_X = 600
QUIT_Y = 500
QUIT_WIDTH = 200
QUIT_HEIGHT = 50
QUIT_TEXT = "Quit"

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
