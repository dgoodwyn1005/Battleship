import pygame
import pygame.image
import Constants as C
import Display as D
import GameGrid
import Button as B
import GameDisplay


class BattleScreen(D.Display):

    def __init__(self):
        super().__init__()
        self.running = True
        self.pause_button = B.Button(C.PAUSE_X, C.PAUSE_Y, C.PAUSE_WIDTH_HEIGHT, C.PAUSE_WIDTH_HEIGHT,
                                     C.PAUSE_TEXT, C.font, C.BLACK_BACKGROUND_COLOR, C.WHITE_FONT_COLOR)
        self.buttons_array = []

        # Load Game Assets
        grid_tile = pygame.image.load(C.IMAGE_FOLDER + "/grid.png")
        self.grid_tile = pygame.transform.scale(grid_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.grid_tile.set_alpha(C.TILE_TRANSPARENCY)
        self.water_tile = pygame.image.load(C.IMAGE_FOLDER + "/water_tile.jpg")
        self.water_tile = pygame.transform.scale(self.water_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))

    # Main Game Loop

    def main_loop(self):

        while self.running:

            for event in pygame.event.get():

                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False
                # Check if it is clicked
                if self.pause_button.is_clicked():
                    print("Clicked")

                # Check if buttons are clicked
                for i in self.buttons_array:
                    if i.is_clicked():
                        print(i.text)



    def create_grid(self):

        # Player and opponent names, and turn message
        player_name = "Player1"
        opponent_name = "Player2"
        turn_message = " Player1"

        # Initialize Game Grid
        grid = GameGrid.gamegrid(C.NUM_ROWS, C.NUM_COL)

        # Draw grid and create buttons at respective locations


        game_display = GameDisplay.GameDisplay(self.screen)

        for x in range(grid.grid_length()):
            for y in range(grid.grid_height()):
                D.Display.blit(self, self.water_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))
                D.Display.blit(self, self.grid_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.font, (0, 0, 0), (101, 100, 100))
                self.buttons_array.append(gridButton)




            # Draw the player turn message
        game_display.draw_turn_indicator(turn_message)

        # Draw the player names in the corners
        game_display.draw_names(player_name, opponent_name)

        # Draw pause button
        self.pause_button.draw(self.screen)



        pygame.display.flip()


battle = BattleScreen()
battle.create_grid()
battle.main_loop()
