import Display as D
import pygame
import Constants as C
import Button as B
import os
import json
import Board as BG
import Account as A
import AccountDisplay as AD
import SoundManager as SM


class LoadGameDisplay(D.Display):

    def __init__(self, username, user=None):
        super().__init__(screenName=C.LOAD_GAME_CAPTION, background=C.BLUE)
        self.load_game_button = B.Button(C.LOAD_SAVED_BUTTON_X + C.LOAD_SAVED_BUTTON_Y, C.LOAD_Y, C.LOAD_WIDTH,
                                         C.LOAD_HEIGHT, C.LOAD_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT, C.FONT,
                                    C.GREY, C.WHITE_FONT_COLOR)
        self.message_label = C.FONT.render("Select a game file to load:", True, C.WHITE_FONT_COLOR)
        self.delete_button = B.Button(C.DELETE_X, C.DELETE_Y, C.DELETE_WIDTH, C.DELETE_HEIGHT, C.DELETE_TEXT, C.FONT,
                                      C.GREY, C.WHITE_FONT_COLOR)
        self.selected_file = ""
        self.username = username
        self.folder_path = C.GAME_FOLDER + self.username
        self.created_buttons = False
        self.screen_buttons = [self.back_button, self.load_game_button, self.delete_button]
        self.total_files = 0
        self.total_background_height = 0
        self.user = user
        self.sounds = SM.Sound()

    def create_buttons(self):
        self.screen.fill(C.BLUE)
        file_y = C.FILE_BUTTON_Y
        if not os.path.exists(self.folder_path):  # Check if the folder exists
            # Display message if no files are found
            self.message_label = C.FONT.render("No saved games found", True, C.RED)
            # Otherwise, show the saved game files store in the file location
        else:
            # Create a background box for the file buttons
            # Get the path to the saved games folder based on the current username
            files = os.listdir(self.folder_path)
            self.total_files = len(files)
            # Create a button for each file in the saved games folder
            for file in files:
                file_button = B.Button(C.FILE_BUTTON_X, file_y + C.FILE_BUTTON_HEIGHT, C.FILE_BUTTON_WIDTH, C.FILE_BUTTON_HEIGHT,
                                       file.split('.')[0], C.FONT, C.GREY, C.WHITE_FONT_COLOR)
                self.screen_buttons.append(file_button)     # Add the button to the list of screen buttons
                file_y += C.FILE_Y_OFFSET      # Increment the y position of the next button

    def load_game(self, save_name):
        """Load the game from a saved file"""
        board = BG.BattleScreen(user=self.user, game_name=save_name, username=self.username)
        with open(self.folder_path + "/" + save_name, "r") as file:
            data = json.load(file)
            board.grid.grid = data["player_grid"]
            board.opponent_grid.grid = data["opponent_grid"]
            if data["current_turn"] == "Player 1":
                board.player_turn = data["current_turn"]
            else:
                board.player_turn = not data["current_turn"]
            count = 0
            for key in data.keys():
                if key.startswith("my_") or key.startswith("opp_"):  # To avoid the grid data and current turn data
                    if count == 5:
                        count = 0  # Reset the count to 0 after going through the first 5 ships
                    if key.startswith("my_"):  # Handles players ships only
                        ship_list = board.ships  # Assign the player ships list
                    else:
                        ship_list = board.opponent_ships  # Assign the opponent ships list
                    ship = ship_list[count]  # Iterate through the ship list
                    ship.head_coordinate = data[key][0]  # Add the head coordinates to each ship
                    ship.rotated = data[key][1]  # Add the direction of the ship
                    ship.sunken = data[key][2]  # Add the sunken status of the ship
                    ship.hit_count = data[key][3]  # Add the hit count of the ship
                    count += 1
            # Update the board with the loaded game data
            board.ship_count = 5
            board.startedBoard = True
            board.placeShips = False
            board.loaded_game = True
            board.signed_in = True
            board.rotate_button.disabled = True
            board.message = "Game loaded successfully"
            self.screen.fill(C.LIGHTER_BLUE_COLOR)
            self.running = False  # Stop the account screen
            board.startDisplay(board.main_loop)  # Start the game screen

    def main_loop(self):
        """The main game loop for the load game screen"""
        self.create_buttons()  # Create the buttons for the saved games
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked():
                        self.running = False
                        person = A.Account(self.username, self.user.password)
                        account_screen = AD.AccountDisplay(person)
                        account_screen.startDisplay(account_screen.main_loop)

            # Switch to hover colors for the buttons if the cursor is over them
            for button in self.screen_buttons:
                if button.is_hovered():
                    button.color = C.HOVER_COLOR
                else:
                    button.color = C.GREY
                if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.sounds.play_sound("click")
                # Handle when only the file buttons are clicked
                if (button.is_clicked() and button != self.load_game_button and button != self.back_button and
                        button != self.delete_button):
                    self.selected_file = button.text
                    self.message_label = C.FONT.render("The current selected game file is: " + self.selected_file,
                                                       True, C.WHITE_FONT_COLOR)
                # Handle when the load game button is clicked
                elif button.is_clicked() and button == self.load_game_button:
                    if self.selected_file != "":
                        self.load_game(self.selected_file + ".json")
                    else:
                        self.message_label = C.FONT.render("Please select a file to load", True, C.RED)
                # Handle when the delete button is clicked
                elif (button.is_clicked() and button == self.delete_button and event.type == pygame.MOUSEBUTTONDOWN
                      and self.user != None):
                    if self.selected_file != "":
                        deleted = self.user.delete_game(self.selected_file + ".json")
                        if deleted:
                            self.message_label = C.FONT.render("File deleted successfully", True, C.WHITE_FONT_COLOR)
                            self.screen_buttons = [btn for btn in self.screen_buttons if btn != self.selected_file]
                            self.selected_file = ""
                        elif deleted == False:
                            self.message_label = C.FONT.render("File already deleted", True, C.RED)
                        else:
                            self.message_label = C.FONT.render("You must be signed in to delete a game", True, C.RED)
                    else:
                        self.message_label = C.FONT.render("Please select a file to delete", True, C.RED)
                # Draw the buttons
                button.draw(self.screen)
            # Draw the message label
            self.screen.blit(self.message_label, (C.LOAD_MESSAGE_X, C.LOAD_MESSAGE_Y))
            pygame.display.flip()
            self.screen.fill(C.BLUE)


if __name__ == "__main__":
    l = LoadGameDisplay("iech")
    l.startDisplay(l.main_loop)
