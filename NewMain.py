# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 20:52:26 2024

@author: alepine
"""

import os
import pygame
import pygame.image

import Display as D
import GameGrid
import Button as B

class BattleScreen(D.Display):

    def __init__(self):
        super().__init__(width= 500, height= 500)
        # CONSTANTS
        self.TILE_WIDTH = 40
        self.TILE_HEIGHT = 40
        self.FONT_COLOR = (255, 255, 255)
        self.FONT_SIZE = 20
        self.running = True
        pygame.init()


# Load Game Assets
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        image_folder = __location__ + "/images"
        grid_tile = pygame.image.load(image_folder + "/grid.png")
        self.grid_tile = pygame.transform.scale(grid_tile, (self.TILE_WIDTH, self.TILE_HEIGHT))
        self.grid_tile.set_alpha(128)

        self.water_tile = pygame.image.load(image_folder + "/water_tile.jpg")
        self.water_tile = pygame.transform.scale(self.water_tile, (self.TILE_WIDTH, self.TILE_HEIGHT))



    # Main Game Loop
    def main_loop(self):
        while self.running:

            for event in pygame.event.get():

                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False

            #screen.fill(background_colour)



    def create_grid(self):

        # Player and opponent names, and turn message
        player_name = "Player1"
        opponent_name = "Player2"
        turn_message = "Turn: Player1"
        running = True

        # Initialize Game Grid
        grid = GameGrid.gamegrid(10, 10)

        # Font for text rendering
        font = pygame.font.Font(None, self.FONT_SIZE)
        # Create pause button
        pause_button = B.Button(480, 480, 20, 20, "Pause", font, (0, 0, 0), (255, 255, 255))
        for x in range(grid.grid_length()):
            for y in range(grid.grid_height()):
                D.Display.blit(self, self.water_tile, (x * self.TILE_WIDTH, y * self.TILE_HEIGHT))
                D.Display.blit(self, self.grid_tile, (x * self.TILE_WIDTH, y * self.TILE_HEIGHT))

        # Draw the player turn message
        turn_text = font.render(turn_message, True, self.FONT_COLOR)
        D.Display.blit(self, turn_text, (D.Display.get_width(self) // 2 - turn_text.get_width() // 2, 20))

        # Draw the player name in the left corner
        player_text = font.render(f"Player: {player_name}", True, self.FONT_COLOR)
        D.Display.blit(self, player_text, (0, 0))

        # Draw the opponent name in the right corner
        opponent_text = font.render(f"Opponent: {opponent_name}", True, self.FONT_COLOR)
        D.Display.blit(self, opponent_text, (D.Display.get_width(self) - opponent_text.get_width(), 0))

        # Draw pause button
        pause_button.draw(self.screen)
        #pause_button.draw(screen)


        # Check if it is clicked
        if pause_button.is_clicked():
            print("Clicked")
        pygame.display.flip()


battle = BattleScreen()
battle.create_grid()
battle.main_loop()

