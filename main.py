#Battleship game using pygame!
#Contains the main game loop


import os
import pygame
import pygame.image
import GameDisplay
import GameGrid
from Button import Button

#CONSTANTS
TILE_WIDTH = 40
TILE_HEIGHT = 40
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 20


background_colour = (0, 0, 0) 
pygame.init()  
#Game Dimensions
#screen = pygame.display.set_mode((1024, 768))
screen = pygame.display.set_mode((500, 500)) 
pygame.display.set_caption("Battleship")
screen.fill(background_colour) 
  
#Load Game Assets
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
image_folder = location + "/images"
grid_tile = pygame.image.load(image_folder + "/grid.png")
grid_tile = pygame.transform.scale(grid_tile, (TILE_WIDTH, TILE_HEIGHT))
grid_tile.set_alpha(128)

water_tile = pygame.image.load(image_folder + "/water_tile.jpg")
water_tile = pygame.transform.scale(water_tile, (TILE_WIDTH, TILE_HEIGHT))

running = True

#Initialize Game Grid
grid = GameGrid.gamegrid(10, 10)

#Font for text rendering
font = pygame.font.Font(None, FONT_SIZE)

# Player and opponent names, and turn message
player_name = "Player1"
opponent_name = "Player2"
turn_message = "Player1"

# Create game display object
game_display = GameDisplay.GameDisplay(screen)

# Create pause button
pause_button = Button(460, 460, 40, 40, "Pause", font, (0, 0, 0), (255, 255, 255))

# Main Game Loop
while running: 
     
    for event in pygame.event.get(): 

        #Keyboard Input
        if event.type == pygame.QUIT: 
            running = False

    screen.fill(background_colour)

    for x in range(grid.grid_length()):
        for y in range(grid.grid_height()):
            screen.blit(water_tile, (x*TILE_WIDTH, y*TILE_HEIGHT))
            screen.blit(grid_tile, (x*TILE_WIDTH, y*TILE_HEIGHT))

            
    # Draw the player turn message
    game_display.draw_turn_indicator(turn_message)
    

    # Draw the player names in the corners
    game_display.draw_names(player_name, opponent_name)


    # Draw pause button
    pause_button.draw(screen)
    
    #Check if it is clicked
    if pause_button.is_clicked():
        print("Clicked")


    pygame.display.flip() 