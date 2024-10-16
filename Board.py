import pygame
import pygame.image
import Constants as C
import Display as D
import GameGrid
import Button as B
import GameDisplay
import Ships as S
import OptionsScreen as OS
import MainMenu as MM



class BattleScreen(D.Display):

    def __init__(self):
        super().__init__()
        self.running = True
        self.placeShips = True
        self.pause_button = B.Button(C.PAUSE_X, C.PAUSE_Y, C.PAUSE_WIDTH_HEIGHT, C.PAUSE_WIDTH_HEIGHT,
                                     C.PAUSE_TEXT, C.font, C.GREY, C.HOVER_COLOR)

        # Load Game Assets

        # Load Grid and Water Tiles
        grid_tile = pygame.image.load(C.IMAGE_FOLDER + "/grid.png")
        self.grid_tile = pygame.transform.scale(grid_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.grid_tile.set_alpha(C.TILE_TRANSPARENCY)
        self.water_tile = pygame.image.load(C.IMAGE_FOLDER + "/water_tile.jpg")
        self.water_tile = pygame.transform.scale(self.water_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.button_list = []

        # Load Ships
        self.carrier_ship = S.Ships("aircraft_carrier", 5)
        self.battle_ship = S.Ships("battleship", 4)
        self.cruiser_ship = S.Ships("cruiser", 3)
        self.submarine_ship = S.Ships("submarine", 2)
        self.destroyer_ship = S.Ships("destroyer", 1)
        self.ships = [self.carrier_ship, self.battle_ship, self.cruiser_ship, self.submarine_ship, self.destroyer_ship]
        self.ship_count = 0




    # Main Game Loop

    def main_loop(self):

        while self.running:

            for event in pygame.event.get():

                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False
                # Check if it is clicked
                if self.pause_button.is_clicked():
                    op_screen = OS.Options_Screen()
                    D.Display.startDisplay(op_screen, op_screen.main_loop)
                    print("Clicked")


                # Check if buttons are clicked
                for button in self.button_list:
                    if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                        # Place ships on the grid
                        if self.placeShips and self.ship_count < 5:
                                current_ship = self.ships[self.ship_count].load_ship_image()
                                ship_size = self.ships[self.ship_count].length
                                # Scale the ship to the correct size based on the ship length
                                current_ship = pygame.transform.scale(current_ship,
                                                                      (C.TILE_WIDTH, C.TILE_HEIGHT*ship_size))
                                D.Display.blit(self, current_ship, (button.x, button.y))
                                self.ship_count += 1
                                pygame.display.flip()
                        elif self.ship_count == 5:
                            self.placeShips = False



            

    def create_grid(self):

        # Player and opponent names, and turn message
        player_name = "Player1"
        opponent_name = "Player2"
        turn_message = "Player1"

        # Create Game Display object
        game_display = GameDisplay.GameDisplay(self.screen)
        game_display.font = C.GAME_FONT

        # Initialize Game Grid
        grid = GameGrid.gamegrid(C.NUM_ROWS, C.NUM_COL)

        #Draw grid and create buttons at respective locations
        for x in range(grid.grid_length()):
            for y in range(grid.grid_height()):
                D.Display.blit(self, self.water_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))
                D.Display.blit(self, self.grid_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.font, C.BLACK_BACKGROUND_COLOR, C.LIGHT_GREY)
                self.button_list.append(gridButton)

            # Draw the grid coordinates
            for x in range(grid.grid_length()):
                coord = C.GAME_FONT.render(str(x + 1), True, C.DARK_GREEN)
                coord_rect = coord.get_rect(center=((x * C.TILE_WIDTH + C.X_OFFSET) + C.TILE_WIDTH / 2, 55))
                self.screen.blit(coord, coord_rect)
            for y in range(grid.grid_height()):
                coord = C.GAME_FONT.render(chr(y + 97), True, C.DARK_GREEN)
                coord_rect = coord.get_rect(center=(30, (y * C.TILE_HEIGHT + C.Y_OFFSET) + C.TILE_HEIGHT / 2))
                self.screen.blit(coord, coord_rect)

        # Draw the player turn message
        game_display.draw_turn_indicator(turn_message)

        # Draw the player names in the corners
        game_display.draw_names(player_name, opponent_name)

        # Draw pause button
        self.pause_button.draw(self.screen)

        pygame.display.flip()


# main_menu = MM.Main_Menu()
# main_menu.main_loop()
battle = BattleScreen()
battle.create_grid()
battle.main_loop()