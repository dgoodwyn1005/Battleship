import Display as D
import pygame
import Constants as C
import Button as B
import os
import json
import Board as BG


class LoadGameDisplay(D.Display):

    def __init__(self, username):
        super().__init__(screenName=C.LOAD_GAME_CAPTION, background=C.BLUE)
        self.load_game_button = B.Button(C.LOAD_SAVED_BUTTON_X + C.LOAD_SAVED_BUTTON_Y, C.LOAD_Y, C.LOAD_WIDTH,
                                         C.LOAD_HEIGHT, C.LOAD_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT, C.FONT,
                                    C.GREY, C.WHITE_FONT_COLOR)
        self.message_label = C.FONT.render("Select a game file to load:", True, C.WHITE_FONT_COLOR)
        self.selected_file = ""
        self.username = username
        self.folder_path = C.GAME_FOLDER + self.username
        self.created_buttons = False
        self.screen_buttons = [self.back_button, self.load_game_button]
        self.total_background_height = 0
        self.board = BG.BattleScreen()

    def create_buttons(self):
        self.screen.fill(C.BLUE)
        # Draw background rectangle behind the file buttons
        if not os.path.exists(self.folder_path):
            self.message_label = C.FONT.render("No saved games found", True, C.RED)
        else:
            pygame.draw.rect(self.screen, C.DARK_GREY, (C.LOAD_X - 10, C.FILE_BUTTON_Y - 10, C.LOAD_WIDTH + 20,
                                                        C.FILE_BUTTON_Y + len(os.listdir(
                                                            self.folder_path)) * C.LOAD_HEIGHT))
            # Get the path to the saved games folder based on the current username
            files = os.listdir(self.folder_path)
            self.total_background_height = len(files) * C.LOAD_HEIGHT
            # Create a button for each file in the saved games folder
            for file in files:
                file_button = B.Button(C.LOAD_X, C.FILE_BUTTON_Y + C.LOAD_HEIGHT, C.LOAD_WIDTH, C.LOAD_HEIGHT,
                                       file.split('.')[0], C.FONT, C.GREY, C.WHITE_FONT_COLOR)
                self.screen_buttons.append(file_button)     # Add the button to the list of screen buttons
                C.FILE_BUTTON_Y += C.FILE_Y_OFFSET      # Increment the y position of the next button

    def load_game(self, save_name):
        """Load the game from a saved file"""
        with open(self.folder_path + "/" + save_name, "r") as file:
            data = json.load(file)
            self.board.grid.grid = data["player_grid"]
            self.board.opponent_grid.grid = data["opponent_grid"]
            if data["current_turn"] == "Player 1":
                self.board.player_turn = data["current_turn"]
            else:
                self.board.player_turn = not data["current_turn"]
            count = 0
            for key in data.keys():
                if key.startswith("my_") or key.startswith("opp_"):  # To avoid the grid data and current turn data
                    if count == 5:
                        count = 0  # Reset the count to 0 after going through the first 5 ships
                    if key.startswith("my_"):  # Handles players ships only
                        ship_list = self.board.ships  # Assign the player ships list
                    else:
                        ship_list = self.board.opponent_ships  # Assign the opponent ships list
                    ship = ship_list[count]  # Iterate through the ship list
                    ship.head_coordinate = data[key][0]  # Add the head coordinates to each ship
                    ship.rotated = data[key][1]  # Add the direction of the ship
                    ship.sunken = data[key][2]  # Add the sunken status of the ship
                    ship.hit_count = data[key][3]  # Add the hit count of the ship
                    count += 1
            self.board.ship_count = 5
            self.board.startedBoard = True
            self.board.placeShips = False
            self.board.loaded_game = True
            self.board.rotate_button.disabled = True
            self.board.message = "Game loaded successfully"
            self.screen.fill(C.LIGHTER_BLUE_COLOR)
            self.running = False  # Stop the account screen
            self.board.startDisplay(self.board.main_loop)  # Start the game screen

    def main_loop(self):
        self.create_buttons()  # Create the buttons for the saved games
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked():
                        self.running = False
            # Draw a background for the file buttons
            pygame.draw.rect(self.screen, C.DARK_GREY,
                             (C.LOAD_X - 10, C.FILE_BUTTON_Y - 80, C.LOAD_WIDTH + 20,
                              self.total_background_height + 40))
            # Switch to hover colors for the buttons if the cursor is over them
            for button in self.screen_buttons:
                if button.is_hovered():
                    button.color = C.HOVER_COLOR
                else:
                    button.color = C.GREY
                # Handle when only the file buttons are clicked
                if button.is_clicked() and button != self.load_game_button and button != self.back_button:
                    self.selected_file = button.text
                    self.message_label = C.FONT.render("The current selected game file is: " + self.selected_file,
                                                       True, C.WHITE_FONT_COLOR)
                # Handle when the load game button is clicked
                elif button.is_clicked() and button == self.load_game_button:
                    if self.selected_file != "":
                        self.load_game(self.selected_file + ".json")
                    else:
                        self.message_label = C.FONT.render("Please select a file to load", True, C.RED)
                # Draw the buttons
                button.draw(self.screen)
            # Draw the message label
            self.screen.blit(self.message_label, (C.LOAD_MESSAGE_X, C.LOAD_MESSAGE_Y))
            pygame.display.flip()
            self.screen.fill(C.BLUE)


if __name__ == "__main__":
    l = LoadGameDisplay("iech")
    l.startDisplay(l.main_loop)
