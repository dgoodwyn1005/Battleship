#Battleship game using pygame!
#Contains the main game loop

import os
import pygame
import pygame.image

import GameGrid

#CONSTANTS
TILE_WIDTH = 40
TILE_HEIGHT = 40

background_colour = (0, 0, 0) 
  
#Game Dimensions
#screen = pygame.display.set_mode((1024, 768))
screen = pygame.display.set_mode((500, 500)) 
pygame.display.set_caption("Battleship")
screen.fill(background_colour) 
  
#Load Game Assets
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
image_folder = __location__ + "/images"
grid_tile = pygame.image.load(image_folder + "/grid.png")
grid_tile = pygame.transform.scale(grid_tile, (TILE_WIDTH, TILE_HEIGHT))
grid_tile.set_alpha(128)

water_tile = pygame.image.load(image_folder + "/water_tile.jpg")
water_tile = pygame.transform.scale(water_tile, (TILE_WIDTH, TILE_HEIGHT))

running = True

#Initialize Game Grid
grid = GameGrid.gamegrid(10, 10)

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

    pygame.display.flip() 