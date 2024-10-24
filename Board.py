import pygame
import pygame.image
import Constants as C
import Display as D
import GameGrid as GG
import Button as B
import GameDisplay
import Ships as S
import OptionsScreen as OS
from Player import CPU




class BattleScreen(D.Display):

    def __init__(self):
        super().__init__()
        self.running = True
        self.placeShips = True
        # turn flag
        self.player_turn = True
        self.pause_button = B.Button(C.PAUSE_X, C.PAUSE_Y, C.PAUSE_WIDTH_HEIGHT, C.PAUSE_WIDTH_HEIGHT,
                                     C.PAUSE_TEXT, C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.rotate_button = B.Button(C.ROTATE_X, C.ROTATE_Y, C.ROTATE_WIDTH_HEIGHT, C.ROTATE_WIDTH_HEIGHT,
                                      C.ROTATE_TEXT, C.font, C.GREY, C.WHITE_FONT_COLOR)

        # Load Game Assets

        # Load Grid and Water Tiles
        grid_tile = pygame.image.load(C.IMAGE_FOLDER + "/grid.png")
        self.grid_tile = pygame.transform.scale(grid_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.grid_tile.set_alpha(C.TILE_TRANSPARENCY)
        self.water_tile = pygame.image.load(C.IMAGE_FOLDER + "/water_tile.jpg")
        self.water_tile = pygame.transform.scale(self.water_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.button_list = []
        # Create Grid object
        self.grid = GG.GameGrid(C.NUM_ROWS, C.NUM_COL)

        # Create Game Display object
        self.game_display = GameDisplay.GameDisplay(self.screen)
        self.game_display.font = C.GAME_FONT

        # Load Ships
        self.carrier_ship = S.Ships("aircraft_carrier", 5)
        self.battle_ship = S.Ships("battleship", 4)
        self.cruiser_ship = S.Ships("cruiser", 3)
        self.submarine_ship = S.Ships("submarine", 2)
        self.destroyer_ship = S.Ships("destroyer", 1)
        self.ships = [self.carrier_ship, self.battle_ship, self.cruiser_ship, self.submarine_ship, self.destroyer_ship]
        self.ship_count = 0
        self.message = "Place " + self.ships[self.ship_count].name + " " + str(self.ships[self.ship_count].length)
        self.ship_preview = self.ships[self.ship_count]
        self.startedBoard = True
        self.create_grid()

        # Create CPU player
        self.cpu_player = CPU(C.NUM_ROWS)


    # Main Game Loop

    def main_loop(self):
        # Draw the ship on the screen
        self.draw_preview_ship()
        while self.running:

            for event in pygame.event.get():

                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False
                if self.player_turn:
                    # Check if it is clicked
                    if self.pause_button.is_clicked():
                        op_screen = OS.Options_Screen()
                        D.Display.startDisplay(op_screen, op_screen.main_loop)
                        self.screen.fill(C.LIGHTER_BLUE_COLOR)
                        self.create_grid()
                        print("Clicked")
                    if self.rotate_button.is_clicked():
                        self.ship_preview.rotated = not self.ship_preview.rotated
                        self.draw_preview_ship()



                    # Check if buttons are clicked
                    for button in self.button_list:
                        if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:

                            # Place ships on the grid
                            if self.placeShips and self.ship_count < 5:
                                    current_ship = self.ships[self.ship_count]
                                    loaded_ship = current_ship.load_ship_image()

                                    # Scale the ship to the correct size based on the ship length
                                    loaded_ship = pygame.transform.scale(loaded_ship,
                                                                      (C.TILE_WIDTH, C.TILE_HEIGHT*current_ship.length))
                                    if current_ship.rotated:
                                        loaded_ship = pygame.transform.rotate(loaded_ship, 90)

                                    tile_check = self.grid.check_tile(button.x//40 - 1, button.y//40 - 1)
                                    # Because the tiles are offset by 40 pixels, we divide by 40 to get the correct grid location
                                    if ((button.y//40 + current_ship.length <= 11 and not current_ship.rotated)
                                            or (button.x//40 + current_ship.length <= 11 and current_ship.rotated)) and tile_check:
                                        self.grid.update_grid(button.x//40 - 1, button.y//40 - 1, current_ship.length, current_ship)

                                        #Update coordinate on ship
                                        current_ship.head_coordinate = (button.x//40 - 1, button.y//40 - 1)

                                        # Draw the ship on the screen
                                        self.screen.blit(loaded_ship, (button.x, button.y))
                                        self.ship_count += 1

                                        # Update the message to display the next ship
                                        if self.ship_count < 5:
                                            self.message = ("Place " + self.ships[self.ship_count].name + " " +
                                                        str(self.ships[self.ship_count].length))

                                            # Update preview ship
                                            self.ship_preview = self.ships[self.ship_count]

                                        # Draw the ship on the screen
                                        self.draw_preview_ship()
                                    else:
                                        # Display message if ship is out of bounds
                                        self.message = "Ship out of bounds: " + str(current_ship.length) + " spaces"
                                        print("Ship out of bounds")
                                    self.game_display.draw_message(self.message)
                                    pygame.display.flip()

                            elif self.ship_count == 5:
                                self.placeShips = False
                                # Player attack action
                                row = button.x // 40 - 1
                                col = button.y // 40 - 1
                                self.player_turn_action(row, col)
                            
            if not self.player_turn:
                # CPU can start making moves
                self.cpu_turn()
            
            if self.pause_button.is_hovered():
                self.pause_button.color = C.HOVER_COLOR
            else:
                self.pause_button.color = C.GREY

            # Redraw the pause button with the updated color
            self.pause_button.draw(self.screen)

            pygame.display.flip()
            self.pause_button.draw(self.screen)

            pygame.display.flip()


    # Handle player turn
    def player_turn_action(self, row, col):
        print(f"Player attacks tile ({row}, {col})")
        result = self.grid.attack_tile(row, col)
        if result:
            print("Player hit a ship!")
        else:
            print("Player missed.")
        
        self.player_turn = False  # End player turn
        pygame.display.flip()
    
    # Handle CPU turn
    def cpu_turn(self):
        print("CPU Turn")
        result = self.cpu_player.make_move(self.grid)
        if result:
            print("Cpu hit a ship")
        else:
            print("Cpu missed")
        self.player_turn = True  # End CPU turn
        pygame.display.flip()


            

    def create_grid(self):

        # Player and opponent names, and turn message
        player_name = "Player1"
        opponent_name = "Player2"
        turn_message = "Player1"


        #Draw grid and create buttons at respective locations
        for x in range(self.grid.grid_length()):
            for y in range(self.grid.grid_height()):
                D.Display.blit(self, self.water_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))
                D.Display.blit(self, self.grid_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.font, C.BLACK_BACKGROUND_COLOR, C.LIGHT_GREY)
                if self.startedBoard:
                    self.button_list.append(gridButton)

            # Draw the grid coordinates
            for x in range(self.grid.grid_length()):
                coord = C.GAME_FONT.render(str(x + 1), True, C.DARK_GREEN)
                coord_rect = coord.get_rect(center=((x * C.TILE_WIDTH + C.X_OFFSET) + C.TILE_WIDTH / 2, 55))
                self.screen.blit(coord, coord_rect)
            for y in range(self.grid.grid_height()):
                coord = C.GAME_FONT.render(chr(y + 97), True, C.DARK_GREEN)
                coord_rect = coord.get_rect(center=(30, (y * C.TILE_HEIGHT + C.Y_OFFSET) + C.TILE_HEIGHT / 2))
                self.screen.blit(coord, coord_rect)
        self.startedBoard = False
        # Draw the player turn message
        self.game_display.draw_turn_indicator(turn_message)

        # Draw the player names in the corners
        self.game_display.draw_names(player_name, opponent_name)

        # Draw pause button
        self.pause_button.draw(self.screen)

        # Draw rotate button
        self.rotate_button.draw(self.screen)

        # Draw the message on the screen
        self.game_display.draw_message(self.message)

        pygame.display.flip()

    def draw_preview_ship(self):
        # Clear previous ship preview by drawing a rectangle
        message_rect = pygame.Rect(C.SHIP_PREVIEW_X, C.SHIP_PREVIEW_Y, C.TILE_WIDTH+200, C.TILE_HEIGHT*5)
        self.screen.fill(C.LIGHTER_BLUE_COLOR, message_rect)

        # Draw the ship on the screen
        if self.ship_count < 5:
            preview = self.ship_preview.load_ship_image()
            if not self.ship_preview.rotated:
                ship = pygame.transform.scale(preview,(C.TILE_WIDTH, C.TILE_HEIGHT*self.ship_preview.length))
                self.screen.blit(ship, (C.SHIP_PREVIEW_X, C.SHIP_PREVIEW_Y))
            else:
                ship = pygame.transform.scale(preview, (C.TILE_WIDTH, C.TILE_HEIGHT*self.ship_preview.length))
                ship = pygame.transform.rotate(ship, 90)
                self.screen.blit(ship, (C.SHIP_PREVIEW_X, C.SHIP_PREVIEW_Y))






if __name__ == "__main__":
    battle = BattleScreen()
    battle.main_loop()

