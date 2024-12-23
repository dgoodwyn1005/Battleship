import os
import pygame
pygame.init()
# CONSTANTS

# IMAGES Folder
IMAGE_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/images"

# FONTS Folder
FONTS_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/fonts"

# AUDIO Folder
AUDIO_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/audio"

# GAME Folder
GAME_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/saved_games/"

# Current Environment
Environment = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Saved Account Document
SAVED_ACCOUNT_DOCUMENT = Environment + "/saved_accounts.json"

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

# DELAYS
TURN_DELAY = 300


# TEXT
WHITE_FONT_COLOR = (255, 255, 255)
FONT_SIZE = 20
FONT = pygame.font.Font(None, FONT_SIZE)    # Font for text rendering

# PAUSE BUTTON
PAUSE_X = 760
PAUSE_Y = 560
PAUSE_WIDTH_HEIGHT = 40
PAUSE_TEXT = "Pause"

# EXIT BUTTON
EXIT_X = 760
EXIT_Y = 610    
EXIT_WIDTH = 40
EXIT_HEIGHT = 40
EXIT_TEXT = "Exit"

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
BLUE = (24, 123, 205)
LIGHT_GREY = (101, 100, 100)
DARK_GREEN = (105, 135, 165)
HOVER_COLOR = (150, 150, 150)
DARK_GREY = (145, 145, 145)

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

# Text box
TEXTBOX_X = 600
TEXTBOX_Y = 180
TEXTBOX_WIDTH = 200
TEXTBOX_HEIGHT = 50
TEXTBOX_TEXT = "Enter Username: "

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
QUIT_Y = 600
QUIT_WIDTH = 200
QUIT_HEIGHT = 50
QUIT_TEXT = "Quit"

# Account button
ACCOUNT_X = 600
ACCOUNT_Y = 500
ACCOUNT_WIDTH = 200
ACCOUNT_HEIGHT = 50
ACCOUNT_B_TEXT = "Account"

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

# Save message
SAVE_MESSAGE_OFFSET = 30

# Save button
SAVE_X = 610
SAVE_Y = 400
SAVE_WIDTH = 200
SAVE_HEIGHT = 60
SAVE_TEXT = "Save"

# Save text field
FILENAME_X = 610
FILENAME_Y = 500
FILENAME_WIDTH = 200
FILENAME_HEIGHT = 60

# Back button
BACK_X = 0
BACK_Y = 0
BACK_WIDTH_HEIGHT = 50
BACK_TEXT = "Back"

# Account
# Text fields
ACCOUNT_CAPTION = "Account"
USERNAME_X = 600
USERNAME_Y = 300
USERNAME_WIDTH = 200
USERNAME_HEIGHT = 50
ACCOUNT_PASSWORD_OFFSET = 100

# Sign in button
SIGN_IN_X = 700
SIGN_IN_Y = 500
SIGN_IN_WIDTH = 200
SIGN_IN_HEIGHT = 50
SIGN_IN_TEXT = "Sign In"

# Register button
REGISTER_X = 495
REGISTER_Y = 500
REGISTER_WIDTH = 200
REGISTER_HEIGHT = 50
REGISTER_TEXT = "Create Account"

# Text next to text fields
USERNAME_TEXT = "Username:"
PASSWORD_TEXT = "Password:"
USER_PASS_OFFSET = 100

# Account message
ACCOUNT_MESSAGE_X = 595
ACCOUNT_MESSAGE_Y = 200
ACCOUNT_TEXT = "Enter your account information"
ACCOUNT_FONT = pygame.font.SysFont(None, 70)

# Account sign in
TOTAL_WINS_TEXT = "Total Wins: "
TOTAL_LOSSES_TEXT = "Total Losses: "

# Load game button
LOAD_X = 600
LOAD_Y = 500
LOAD_WIDTH = 200
LOAD_HEIGHT = 50
LOAD_TEXT = "Load Game"

# Start game button offset
START_OFFSET_X = 300
START_OFFSET_Y = 200

# Reset password button
RESET_PASS_TEXT = "Reset Password"
RESET_PASS_X = 600
RESET_PASS_Y = 700
RESET_PASS_WIDTH = 200
RESET_PASS_HEIGHT = 50

# Reset password text field
RESET_TEXT_X = 600
RESET_TEXT_Y = 630
RESET_TEXT_WIDTH = 200
RESET_TEXT_HEIGHT = 50

# Sign out button
SIGN_OUT_TEXT = "Sign Out"
SIGN_OUT_X = 900
SIGN_OUT_Y = 500
SIGN_OUT_WIDTH = 200
SIGN_OUT_HEIGHT = 50

# Load Game Display
LOAD_GAME_CAPTION = "Load Game"

# File buttons
FILE_BUTTON_Y = 100
FILE_BUTTON_X = 600
FILE_BUTTON_WIDTH = 200
FILE_BUTTON_HEIGHT = 50
FILE_Y_OFFSET = 60

# Load Button
LOAD_SAVED_BUTTON_X = 500
LOAD_SAVED_BUTTON_Y = 500
LOAD_MESSAGE_X = 610
LOAD_MESSAGE_Y = 100

# Delete Button
DELETE_X = 200
DELETE_Y = 500
DELETE_WIDTH = 200
DELETE_HEIGHT = 50
DELETE_TEXT = "Delete"
