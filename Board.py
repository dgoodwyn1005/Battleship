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
import SoundManager as SM
from Player import CPU


class BattleScreen(D.Display):

    def __init__(self, username="Player1"):
        super().__init__()
        self.username = username
        self.placeShips = True
        self.player_turn = True  # turn flag that swtiches between player and CPU
        self.game_over = False
        self.turn_message = self.username
        self.pause_button = B.Button(C.PAUSE_X, C.PAUSE_Y, C.PAUSE_WIDTH_HEIGHT, C.PAUSE_WIDTH_HEIGHT,
                                     C.PAUSE_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.rotate_button = B.Button(C.ROTATE_X, C.ROTATE_Y, C.ROTATE_WIDTH_HEIGHT, C.ROTATE_WIDTH_HEIGHT,
                                      C.ROTATE_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)

        # Load Game Assets

        # self.sounds = SM.Sound()        # This is the reason for the black screen. The sound is not being loaded properly

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
        self.opponent_attacks = set()
        self.my_attacks = set()

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
        self.player_ships_remaining = 5
        self.ship_count = 0
        self.message = "Place " + self.ships[self.ship_count].name + " " + str(self.ships[self.ship_count].length)
        self.ship_preview = self.ships[self.ship_count]
        self.startedBoard = True
        self.loaded_game = False

        # Load Opponent Ships
        self.opponent_carrier_ship = S.Ships("aircraft_carrier", 5)
        self.opponent_battle_ship = S.Ships("battleship", 4)
        self.opponent_cruiser_ship = S.Ships("cruiser", 3)
        self.opponent_submarine_ship = S.Ships("submarine", 2)
        self.opponent_destroyer_ship = S.Ships("destroyer", 1)
        self.opponent_ships = [self.opponent_carrier_ship, self.opponent_battle_ship, self.opponent_cruiser_ship,
                               self.opponent_submarine_ship, self.opponent_destroyer_ship]
        self.cpu_ships_remaining = 5
        # Create CPU player
        self.cpu_player = CPU(C.NUM_ROWS)

    def check_win_condition(self):
        """Check if the game has been won"""
        if self.player_ships_remaining == 0:
            self.message = "CPU Wins!"
            self.game_display.draw_message(self.message)
            pygame.display.flip()
            self.game_over = True
            #self.running = False
        elif self.cpu_ships_remaining == 0:
            self.message = "{} Wins!".format(self.username)
            self.game_display.draw_message(self.message)
            pygame.display.flip()
            self.game_over = True
            #self.running = False
    # Main Game Loop
    def main_loop(self):
        pygame.display.flip()
        self.create_grid() # Draw the grid on the screen
        self.draw_preview_ship() # Draw the ship on the screen
        if not self.loaded_game:    # If the game is not loaded, place CPU ships
            self.cpu_place_ships()         # Place CPU ships on the grid
        else:       # Redraw the loaded game
            self.redraw_loaded_game(self.grid, C.X_OFFSET, C.Y_OFFSET, self.button_list, True)
            self.redraw_loaded_game(self.opponent_grid, C.OPPONENT_X_OFFSET, C.OPPONENT_Y_OFFSET,
                                    self.opponent_button_list, False)
        # self.sounds.play_song("conflict")
        while self.running:
            for event in pygame.event.get():
                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False
                # Check if it is clicked
                if self.pause_button.is_clicked():
                    # Pass the grids and current turn to the Options Screen in case the user wants to save the game
                    op_screen = OS.Options_Screen(self.grid.grid, self.opponent_grid.grid, self.player_turn,
                                                  self.ships, self.opponent_ships)
                    op_screen.startDisplay(op_screen.main_loop)
                    # Redraw Board screen after returning from the Pause Menu

                    self.screen.fill(C.LIGHTER_BLUE_COLOR)      # Fill screen with light blue color
                    self.create_grid()                          # Draw the grids again
                    self.redraw_ships()                         # Redraw the ships
                    self.draw_preview_ship()               # Draw the preview ship if the player is still placing ships
                    self.redraw_attacks(self.my_attacks)    # Redraw the attacks on the opponent grid
                    self.redraw_attacks(self.opponent_attacks)  # Redraw the attacks on the player grid
                    self.redraw_sunken_ships()              # Redraw the sunken ships
                    # self.sounds.stop_song("conflict")
                if self.rotate_button.is_clicked():     # Rotate the ship if the rotate button is clicked
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
                                            self.message = "Ships placed. Begin attacking!"
                                            self.rotate_button.disabled = True  # Disable the rotate button

                                        # Draw the ship on the screen
                                        self.draw_preview_ship()
                                    else:
                                        self.message = "Overlaps with another ship"

                                else:
                                    # Display message if ship is out of bounds
                                    self.message = "Ship out of bounds: " + str(current_ship.length) + " spaces"
                                self.game_display.draw_message(self.message)
                                pygame.display.flip()

                    # Update turn message
                    if self.player_turn:
                        self.turn_message = self.username
                    else:
                        self.turn_message = "CPU"

                    # Check if the player has clicked on the opponent grid after ships have been placed
                    if self.player_turn and not self.placeShips:
                        for opponent_button in self.opponent_button_list:
                            if opponent_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN and not opponent_button.disabled:
                                row = (opponent_button.x - C.OPPONENT_X_OFFSET) // C.TILE_WIDTH
                                col = (opponent_button.y - C.OPPONENT_Y_OFFSET) // C.TILE_HEIGHT
                                self.player_turn_action(row, col)
                                opponent_button.disabled = True     # Disable the button after it has been clicked
                                self.turn_message = "CPU"
                                self.game_display.draw_turn_indicator(self.turn_message)
                                pygame.display.flip()

                if not self.player_turn and not self.placeShips:    # CPU turn begins after all ships have been placed and player has attacked
                    # CPU can start making moves
                    self.cpu_turn()
                    self.turn_message = self.username
                    self.game_display.draw_turn_indicator(self.turn_message)
                    pygame.display.flip()


            # Check if the pause button is hovered and change color accordingly
            if self.pause_button.is_hovered():
                self.pause_button.color = C.HOVER_COLOR
            else:
                self.pause_button.color = C.GREY

            # Check if the rotate button is hovered and change color accordingly
            if self.rotate_button.is_hovered() and not self.rotate_button.disabled:
                self.rotate_button.color = C.HOVER_COLOR
            elif self.rotate_button.disabled:
                self.rotate_button.color = C.LIGHTER_BLUE_COLOR
                self.rotate_button.text_color = C.LIGHTER_BLUE_COLOR
            else:
                self.rotate_button.color = C.GREY

            # Redraw the pause button and rotate button with the updated color
            self.pause_button.draw(self.screen)
            self.rotate_button.draw(self.screen)
            self.game_display.draw_turn_indicator(self.turn_message)

            self.pause_button.draw(self.screen)
            pygame.display.flip()

    # Handle player turn
    def player_turn_action(self, row, col):
        print(f"Player attacks tile ({row}, {col})")
        result = self.opponent_grid.attack_tile(row, col)      # Attack the tile and returns the result
        row = row * C.TILE_WIDTH + C.OPPONENT_X_OFFSET      # Convert row and col to x and y coordinates
        col = col * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET
        if result != -1:
            self.message = "{} hit a ship!".format(self.username)     # Update message if player hits a ship
            self.opponent_ships[5 - result].hit_count += 1  # Increase hit count of ship
            self.my_attacks.add((row, col, "hit"))      # Add x and y coordinates and hit to my_attacks
            self.screen.blit(self.explosion, (row, col))   # Draw explosion
            # Put play explosion method in this line
            checkSunken = self.opponent_ships[5 - result].check_sunken()  # Check if ship is sunken
            if checkSunken:
                self.show_sunken_ship(self.opponent_ships[5 - result])
            # self.sounds.play_sound("explosion")
            
            # self.sounds.play_sound("explosion")               Need to fix sound module
        else:
            self.message = "{} missed.".format(self.username)  # Update message if player misses
            self.my_attacks.add((row, col, "miss"))  # Add x and y coordinates and miss to my_attacks
            self.screen.blit(self.water_ripple, (row, col))  # Draw water ripple
            # self.sounds.play_sound("splash")
        self.game_display.draw_message(self.message)        # Draws the result message on the screen

        self.player_turn = False  # End player turn
        self.turn_message = "CPU"
        pygame.display.flip()
        pygame.time.delay(100)


    # Handle CPU turn
    def cpu_turn(self):
        """CPU makes a move and it displays on the 1st player's grid"""
        try:  # For testing purposes, if all tiles have been attacked, the game will not crash
            result = self.cpu_player.make_move(self.grid)
            row = result[1][0] * C.TILE_WIDTH + C.X_OFFSET
            col = result[1][1] * C.TILE_HEIGHT + C.Y_OFFSET
            if result[0] != -1:
                self.message = "Cpu hit a ship"
                self.ships[result[0] - 1].hit_count += 1
                self.opponent_attacks.add((row, col, "hit"))
                self.screen.blit(self.explosion, (row, col))
                # self.sounds.play_sound("explosion")
                # Check if the ship is sunken
                if self.ships[int(result[0]) - 1].check_sunken():
                    self.player_ships_remaining -= 1
                self.check_win_condition()
            else:
                self.message = "CPU missed."
                self.opponent_attacks.add((row, col, "miss"))
                self.screen.blit(self.water_ripple, (row, col))
                # self.sounds.play_sound("splash")
        except:  # If all tiles have been attacked, the game will not crash
            print("All tiles have been attacked")
        self.player_turn = True  # End CPU turn
        self.turn_message = self.username
        pygame.display.flip()
        pygame.time.delay(400)

    def create_grid(self):
        """Draws both grids onto the screen, creates buttons for each tile, and them to a list"""
        # Player and opponent names, and turn message
        player_name = self.username
        opponent_name = "CPU"
        self.game_display.draw_names(player_name, opponent_name)
        #Draw grid and create buttons at respective locations
        for x in range(self.grid.grid_length()):
            for y in range(self.grid.grid_height()):
                self.screen.blit(self.water_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))
                self.screen.blit(self.grid_tile, (x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.X_OFFSET, y * C.TILE_HEIGHT + C.Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.FONT, C.BLACK_BACKGROUND_COLOR, C.LIGHT_GREY)
                if self.startedBoard:       # Add buttons to list only when the board is first created to avoid duplicates
                    self.button_list.append(gridButton) # Otherwise it tries to add the same buttons multiple times and causes problems


        # Draw the opponent's grid
        for x in range(self.opponent_grid.grid_length()):
            for y in range(self.opponent_grid.grid_height()):
                self.screen.blit(self.water_tile, (x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET))
                self.screen.blit(self.grid_tile, (x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET))

                # Add buttons to list
                gridButton = B.Button(x * C.TILE_WIDTH + C.OPPONENT_X_OFFSET, y * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET, C.TILE_WIDTH,
                                      C.TILE_HEIGHT, chr(y + 97) + str(x + 1), C.FONT, C.BLACK_BACKGROUND_COLOR,
                                      C.LIGHT_GREY)
                if self.startedBoard:   # Add buttons to list only when the board is first created to avoid duplicates
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

        # Update the display
        pygame.display.flip()

    def draw_preview_ship(self):
        """Draw the preview ship on the screen so that the player knows which ship is being placed"""
        # Clear previous ship preview by drawing a rectangle over it
        message_rect = pygame.Rect(C.SHIP_PREVIEW_X, C.SHIP_PREVIEW_Y, C.TILE_WIDTH+200, C.TILE_HEIGHT*5)
        self.screen.fill(C.LIGHTER_BLUE_COLOR, message_rect)

        # Draw the ship on the screen
        if self.ship_count < 5:     # If all ships have not been placed, draw the preview image of the next ship
            preview = self.ship_preview.load_ship_image()
            if not self.ship_preview.rotated:     # If the ship is not rotated, draw the ship normally
                ship = pygame.transform.scale(preview,(C.TILE_WIDTH, C.TILE_HEIGHT*self.ship_preview.length))
                self.screen.blit(ship, (C.SHIP_PREVIEW_X, C.SHIP_PREVIEW_Y))
            else:       # Otherwise, rotate the ship image and draw it
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
            placed = False
            while not placed:
                rotated = random.choice([True, False])  # Randomly choose if the ship should be rotated
                ship.rotated = rotated      # Set the ship attribute as rotated or not
                if not ship.rotated:
                    row = random.randint(0, self.opponent_grid.grid_length() - 1)
                    col = random.randint(0, self.opponent_grid.grid_height() - ship.length)
                else:
                    row = random.randint(0, self.opponent_grid.grid_length() - ship.length)
                    col = random.randint(0, self.opponent_grid.grid_height() - 1)
                # Check if the ship can be placed on the grid
                canPlace = self.opponent_grid.check_tile(row, col, ship.length, ship.rotated)
                if canPlace:
                    self.opponent_grid.update_grid(row, col, ship.length, ship)
                    ship.head_coordinate = (row * C.TILE_WIDTH + C.OPPONENT_X_OFFSET,
                                            col * C.TILE_HEIGHT + C.OPPONENT_Y_OFFSET)
                    placed = True
        print(self.opponent_grid.grid)

    def show_sunken_ship(self, ship):
        """Show the sunken ship on the screen"""
        sunken_ship = ship.load_ship_image()
        sunken_ship = pygame.transform.scale(sunken_ship,  # Scale the sunken ship to the correct size based on ship
                                             (C.TILE_WIDTH, C.TILE_HEIGHT * ship.length))
        if ship.rotated:                # Rotate the ship if it is supposed to be rotated
            sunken_ship = pygame.transform.rotate(sunken_ship, 90)
        sunken_ship.set_alpha(100)      # Set the transparency of the sunken ship
        self.screen.blit(sunken_ship, ship.head_coordinate)  # Draw the sunken ship on the screen
        ship.sunken = True              # Set the ship as sunken
        pygame.display.flip()

    def redraw_attacks(self, coord_set):
        """Redraw the attacks on the screen after returning from the pause screen"""
        for coord in coord_set:
            if coord[2] == "hit":    # Draw explosion if the attack was a hit
                self.screen.blit(self.explosion, (coord[0], coord[1]))
            else:                   # Otherwise, draw the water ripple if the attack was a miss
                self.screen.blit(self.water_ripple, (coord[0], coord[1]))
        pygame.display.flip()

    def redraw_sunken_ships(self):
        """Redraw the sunken ships on the screen after returning from the pause menu screen"""
        for ship in self.opponent_ships:    # Iterate through all ships
            if ship.sunken:           # If the ship is sunken, draw the sunken ship
                self.show_sunken_ship(ship)
        pygame.display.flip()

    def redraw_loaded_game(self, grid: GG.GameGrid, x_offset, y_offset, button_list, cpu_player):
        """Redraw the loaded game on the screen"""
        for button in button_list:
            for x in range(grid.grid_length()):
                for y in range(grid.grid_length()):
                    # Adds the offset of the grid to the x and y coordinates
                    offset_x = x * C.TILE_WIDTH + x_offset
                    offset_y = y * C.TILE_HEIGHT + y_offset
                    if grid.grid[x][y] == 6:   # Show the hit tiles
                        self.screen.blit(self.explosion, (offset_x, offset_y))      # Draw the explosion
                        if button.x == offset_x and button.y == offset_y:     # Disable the button if it has been attacked
                            button.disabled = True
                            if cpu_player:  # If the player is the CPU, add the attacks to the opponent_attacks set
                                self.cpu_player.attacked_coords.add((x, y))
                                self.opponent_attacks.add((offset_x, offset_y, "hit"))
                            else:  # Otherwise, add the attacks to the my_attacks set
                                self.my_attacks.add((offset_x, offset_y, "hit"))
                    elif grid.grid[x][y] == 7:     # Show the missed tiles
                        self.screen.blit(self.water_ripple, (offset_x, offset_y))       # Draw the water ripple
                        if button.x == offset_x and button.y == offset_y:    # Disable the button if it has been attacked
                            button.disabled = True
                        if cpu_player:    # If the player is the CPU, add the attacks to the opponent_attacks set
                            self.cpu_player.attacked_coords.add((x, y, "miss"))
                        else:       # Otherwise, add the attacks to the my_attacks set
                            self.my_attacks.add((offset_x, offset_y, "miss"))





if __name__ == "__main__":
    battle = BattleScreen()
    battle.startDisplay(battle.main_loop)
