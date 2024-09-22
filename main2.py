# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 20:52:26 2024

@author: alepine
"""

import os
import pygame
import pygame.image

import GameGrid
import Button

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

#Font for text rendering
font = pygame.font.Font(None, FONT_SIZE)

# Player and opponent names, and turn message
player_name = "Player1"
opponent_name = "Player2"
turn_message = "Turn: Player1"

# Create pause button
pause_button = Button(480, 480, 20, 20, "Pause", font, (0, 0, 0), (255, 255, 255))

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
    turn_text = font.render(turn_message, True, FONT_COLOR)
    screen.blit(turn_text, (screen.get_width() // 2 - turn_text.get_width() // 2, 20))

    # Draw the player name in the left corner
    player_text = font.render(f"Player: {player_name}", True, FONT_COLOR)
    screen.blit(player_text, (0, 0))

    # Draw the opponent name in the right corner
    opponent_text = font.render(f"Opponent: {opponent_name}", True, FONT_COLOR)
    screen.blit(opponent_text, (screen.get_width() - opponent_text.get_width(), 0))


    # Draw pause button
    pause_button.draw(screen)
    
    #Check if it is clicked
    if pause_button.is_clicked():
        print("Clicked")


    pygame.display.flip() 