import random

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
        self.placeShips = True
        # turn flag
        self.player_turn = True
        self.pause_button = B.Button(C.PAUSE_X, C.PAUSE_Y, C.PAUSE_WIDTH_HEIGHT, C.PAUSE_WIDTH_HEIGHT,
                                     C.PAUSE_TEXT, C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.rotate_button = B.Button(C.ROTATE_X, C.ROTATE_Y, C.ROTATE_WIDTH_HEIGHT, C.ROTATE_WIDTH_HEIGHT,
                                      C.ROTATE_TEXT, C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.turn_message = "Player1"

        # Load Game Assets

        # Load Grid and Water Tiles
        grid_tile = pygame.image.load(C.IMAGE_FOLDER + "/grid.png")
        self.grid_tile = pygame.transform.scale(grid_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.grid_tile.set_alpha(C.TILE_TRANSPARENCY)
        self.water_tile = pygame.image.load(C.IMAGE_FOLDER + "/water_tile.jpg")
        self.water_tile = pygame.transform.scale(self.water_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.button_list = []
        self.opponent_button_list = []

        # Load and Scale Explosion and Water images
        self.explosion = pygame.image.load(C.IMAGE_FOLDER + "/explosion.jpg")
        self.water_ripple = pygame.image.load(C.IMAGE_FOLDER + "/ripple.jpg")
        self.explosion = pygame.transform.scale(self.explosion, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.water_ripple = pygame.transform.scale(self.water_ripple, (C.TILE_WIDTH, C.TILE_HEIGHT))


        # Create Grid object
        self.grid = GG.GameGrid(C.NUM_ROWS, C.NUM_COL)
        self.opponent_grid = GG.GameGrid(C.NUM_ROWS, C.NUM_COL)

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


        # Load Opponent Ships
        self.opponent_carrier_ship = S.Ships("aircraft_carrier", 5)
        self.opponent_battle_ship = S.Ships("battleship", 4)
        self.opponent_cruiser_ship = S.Ships("cruiser", 3)
        self.opponent_submarine_ship = S.Ships("submarine", 2)
        self.opponent_destroyer_ship = S.Ships("destroyer", 1)
        self.opponent_ships = [self.opponent_carrier_ship, self.opponent_battle_ship, self.opponent_cruiser_ship,
                               self.opponent_submarine_ship, self.opponent_destroyer_ship]

        # Create CPU player
        self.cpu_player = CPU(C.NUM_ROWS)

        # The self.options messes up the display of the board screen. We need help to fix this
        # self.options = OS.Options_Screen()



    # Main Game Loop
    def main_loop(self):
        self.cpu_place_ships()         # Place CPU ships
        self.create_grid() # Draw the grid on the screen
        self.draw_preview_ship() # Draw the ship on the screen
        while self.running:

            for event in pygame.event.get():

                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False

                # Check if it is clicked
                if self.pause_button.is_clicked():
                    op_screen = OS.Options_Screen()
                    op_screen.startDisplay(op_screen.main_loop)
                    self.screen.fill(C.LIGHTER_BLUE_COLOR)
                    self.create_grid()
                    self.redraw_ships()
                    self.draw_preview_ship()
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

                                # Because the tiles are offset by 40 pixels, we divide by 40 to get the correct grid location
                                if ((button.y//C.TILE_HEIGHT + current_ship.length <= 11 and not current_ship.rotated)
                                        or (button.x//C.TILE_HEIGHT + current_ship.length <= 11 and current_ship.rotated)):

                                    # Check if the ship can be placed on the grid (i.e. if it does not overlap with another ship)
                                    tile_check = self.grid.check_tile(button.x // C.TILE_HEIGHT - 1, button.y // C.TILE_HEIGHT - 1,
                                                                      current_ship.length, current_ship.rotated)

                                    if tile_check:
                                        # Update the grid with the ship
                                        self.grid.update_grid(button.x//C.TILE_HEIGHT - 1, button.y//C.TILE_HEIGHT - 1, current_ship.length, current_ship)

                                        #Update coordinate on ship
                                        current_ship.head_coordinate = (button.x, button.y)

                                        # Draw the ship on the screen
                                        self.screen.blit(loaded_ship, (button.x, button.y))
                                        self.ship_count += 1

                                        # Update the message to display the next ship
                                        if self.ship_count < 5:
                                            self.message = ("Place " + self.ships[self.ship_count].name + " " +
                                                        str(self.ships[self.ship_count].length))

                                            # Update preview ship
                                            self.ship_preview = self.ships[self.ship_count]


                                        else: # If all ships have been placed this allows the attacking to begin
                                            self.placeShips = False

                                        # Draw the ship on the screen
                                        self.draw_preview_ship()
                                    else:
                                        self.message = "Overlaps with another ship"

                                else:
                                    # Display message if ship is out of bounds
                                    self.message = "Ship out of bounds: " + str(current_ship.length) + " spaces"
                                self.game_display.draw_message(self.message)
                                pygame.display.flip()

                    # Player can start making moves



                    if self.player_turn and not self.placeShips:
                        for opponent_button in self.opponent_button_list:
                            if opponent_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN and not opponent_button.disabled:
                                row = (opponent_button.x - C.OPPONENT_X_OFFSET) // C.TILE_WIDTH
                                col = (opponent_button.y - C.OPPONENT_Y_OFFSET) // C.TILE_HEIGHT
                                self.player_turn_action(row, col)
                                opponent_button.disabled = True     # Disable the button after it has been clicked

                if not self.player_turn and not self.placeShips:
                    # CPU can start making moves
                    self.cpu_turn()


            # Check if the pause button is hovered and change color accordingly
            if self.pause_button.is_hovered():
                self.pause_button.color = C.HOVER_COLOR
            else:
                self.pause_button.color = C.GREY

            # Check if the rotate button is hovered and change color accordingly
            if self.rotate_button.is_hovered():
                self.rotate_button.color = C.HOVER_COLOR
            else:
                self.rotate_button.color = C.GREY

            # Redraw the pause button and rotate button with the updated color
            self.pause_button.draw(self.screen)
            self.rotate_button.draw(self.screen)
            self.game_display.draw_turn_indicator(self.turn_message)

            pygame.display.flip()


    # Handle player turn
    def player_turn_action(self, row, col):
        print(f"Player attacks tile ({row}, {col})")
        result = int(self.opponent_grid.attack_tile(row, col))
        print("This is the result", result)
        if result != -1:
            self.message = "Player hit a ship!"
            self.opponent_ships[5 - result].hit_count += 1  # Increase hit count of ship
            print()
            print("Ship number is " + str(5 - result))
            self.screen.blit(self.explosion, (row * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, col * C.TILE_HEIGHT
                                              + C.OPPONENT_Y_OFFSET))   # Draw explosion
            # Put play explosion method in this line
            checkSunken = self.opponent_ships[5-result].check_sunken()  # Check if ship is sunken
            print(self.opponent_ships[5 - result].name + " is sunken: " + str(checkSunken))
            if checkSunken:
                self.show_sunken_ship(self.opponent_ships[5-result])

        else:
            self.message = "Player missed."
            self.screen.blit(self.water_ripple, (row * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, col * C.TILE_HEIGHT
                                                 + C.OPPONENT_Y_OFFSET))  # Draw water ripple
            # Put the play water sound method in this line
        self.game_display.draw_message(self.message)

        self.player_turn = False  # End player turn
        self.turn_message = "CPU"


    # Handle CPU turn
    def cpu_turn(self):
        # print("CPU Turn")
        result = self.cpu_player.make_move(self.grid)
        if result[0] != -1:
            # print("Cpu hit a ship")
            self.ships[int(result[0]) - 1].hit_count += 1
            self.screen.blit(self.explosion, (result[1][0] * C.TILE_WIDTH + C.X_OFFSET, result[1][1] * C.TILE_HEIGHT + C.Y_OFFSET))
        else:
            # print("Cpu missed")
            self.screen.blit(self.water_ripple, (result[1][0] * C.TILE_WIDTH + C.X_OFFSET, result[1][1] * C.TILE_HEIGHT + C.Y_OFFSET))
        self.player_turn = True  # End CPU turn
        self.turn_message = "Player1"
        pygame.display.flip()

            

    def create_grid(self):

        # Player and opponent names, and turn message
        player_name = "Player1"
        opponent_name = "Player2"



        #Draw grid and create buttons at respective locations
        for x in range(self.grid.grid_length()):
            for y in range(self.grid.grid_height()):
                self.screen.blit(self.water_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))
                self.screen.blit(self.grid_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.font, C.BLACK_BACKGROUND_COLOR, C.LIGHT_GREY)
                if self.startedBoard:       # Add buttons to list only when the board is first created to avoid duplicates
                    self.button_list.append(gridButton) # Otherwise it tries to add the same buttons multiple times and causes problems


        # Draw the opponent's grid
        for x in range(self.opponent_grid.grid_length()):
            for y in range(self.opponent_grid.grid_height()):
                self.screen.blit(self.water_tile, (x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET))
                self.screen.blit(self.grid_tile, (x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.font, C.BLACK_BACKGROUND_COLOR,
                                      C.LIGHT_GREY)
                if self.startedBoard:
                    self.opponent_button_list.append(gridButton)

        # Draw the grid coordinates
        for x in range(self.grid.grid_length()):
            coord = C.GAME_FONT.render(str(x + 1), True, C.DARK_GREEN)
            coord_rect = coord.get_rect(center=((x * C.TILE_WIDTH + C.X_OFFSET) + C.TILE_WIDTH / 2, 55))
            self.screen.blit(coord, coord_rect)
        for y in range(self.grid.grid_height()):
            coord = C.GAME_FONT.render(chr(y + 97), True, C.DARK_GREEN)
            coord_rect = coord.get_rect(center=(30, (y * C.TILE_HEIGHT + C.Y_OFFSET) + C.TILE_HEIGHT / 2))
            self.screen.blit(coord, coord_rect)

        # Draw the opponent grid coordinates
        for x in range(self.opponent_grid.grid_length()):
            coord = C.GAME_FONT.render(str(x + 1), True, C.DARK_GREEN)
            coord_rect = coord.get_rect(center=((x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET) + C.TILE_WIDTH / 2, 55))
            self.screen.blit(coord, coord_rect)
        for y in range(self.opponent_grid.grid_height()):
            coord = C.GAME_FONT.render(chr(y + 97), True, C.DARK_GREEN)
            coord_rect = coord.get_rect(center=(875, (y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET) + C.TILE_HEIGHT / 2))
            self.screen.blit(coord, coord_rect)

        # The variable that stops the buttons from being added multiple times
        self.startedBoard = False

        # Draw the player turn message
        self.game_display.draw_turn_indicator(self.turn_message)

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

    def redraw_ships(self):
        """Redraw the ships on the screen after returning from the pause screen"""
        for ship in self.ships:
            if ship.head_coordinate != (-1, -1):
                # Load the ship image
                loaded_ship = ship.load_ship_image()
                loaded_ship = pygame.transform.scale(loaded_ship,
                                                     (C.TILE_WIDTH, C.TILE_HEIGHT * ship.length))
                # Rotate the ship if it is supposed to be rotated
                if ship.rotated:
                    loaded_ship = pygame.transform.rotate(loaded_ship, 90)
                # Draw the ship on the screen
                self.screen.blit(loaded_ship, (ship.head_coordinate[0],
                                               ship.head_coordinate[1]))

    def cpu_place_ships(self):
        """Place the CPU ships on the opponent grid"""
        for ship in self.opponent_ships:

            rotated = random.choice([True, False])      # Randomly choose if the ship should be rotated
            ship.rotated = rotated

            rowCheck = False
            while not rowCheck:     # Check if the ship can be placed in the row
                row = random.randint(0, 9)
                if not ship.rotated:
                    rowCheck = True
                elif ship.rotated and row + ship.length <= 10:
                    rowCheck = True

            colCheck = False
            while not colCheck:     # Check if the ship can be placed in the column
                col = random.randint(0, 9)
                if col + ship.length <= 10:
                    colCheck = True


            canPlace = self.opponent_grid.check_tile(row, col, ship.length, ship.rotated)  #Check if the ship can be placed
            if canPlace:
                self.opponent_grid.update_grid(row, col, ship.length, ship)     # Update the grid with the ship
                ship.head_coordinate = (row * C.TILE_WIDTH + C.OPPONENT_X_OFFSET,
                                    col * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET)
        print(self.opponent_grid.grid)

    def show_sunken_ship(self, ship):
        """Show the sunken ship on the screen"""
        sunken_ship = ship.load_ship_image()
        sunken_ship = pygame.transform.scale(sunken_ship,
                                             (C.TILE_WIDTH, C.TILE_HEIGHT * ship.length))
        if ship.rotated:                # Rotate the ship if it is supposed to be rotated
            sunken_ship = pygame.transform.rotate(sunken_ship, 90)
        sunken_ship.set_alpha(100)      # Set the transparency of the sunken ship
        self.screen.blit(sunken_ship, ship.head_coordinate)
        pygame.display.flip()


if __name__ == "__main__":
    battle = BattleScreen()
    battle.startDisplay(battle.main_loop())


