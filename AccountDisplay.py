import Display as D
import pygame
import Constants as C
import Button as B
import Account
import Board as BG
import json
from textbox import TextBox
import SignIn as SI


class AccountDisplay(D.Display):
    def __init__(self, user: Account.Account):
        super().__init__(screenName=C.ACCOUNT_CAPTION, background=C.BLUE)
        self.user = user
        # Create the title label
        self.title = C.FONT.render(C.ACCOUNT_CAPTION, True, C.WHITE_FONT_COLOR)
        self.text_username_label = C.FONT.render(C.USERNAME_TEXT, True, C.WHITE_FONT_COLOR)
        self.username = C.FONT.render(self.user.username, True, C.WHITE_FONT_COLOR)
        # Create the total wins label and text
        self.total_wins_label = C.FONT.render(C.TOTAL_WINS_TEXT + str(self.user.total_wins), True, C.WHITE_FONT_COLOR)
        # Create the total losses label and text
        self.total_losses_label = C.FONT.render(C.TOTAL_LOSSES_TEXT + str(self.user.total_losses), True,
                                                C.WHITE_FONT_COLOR)
        # Create the reset password button
        self.reset_pass_button = B.Button(C.RESET_PASS_X, C.RESET_PASS_Y, C.RESET_PASS_WIDTH, C.RESET_PASS_HEIGHT,
                                          C.RESET_PASS_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        # Create the load games button
        self.load_game_button = B.Button(C.LOAD_X, C.LOAD_Y, C.LOAD_WIDTH, C.LOAD_HEIGHT, C.LOAD_TEXT,
                                         C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        # Create the reset password text field
        self.reset_password_textbox = TextBox(C.RESET_TEXT_X, C.RESET_TEXT_Y, C.RESET_TEXT_WIDTH,
                                           C.RESET_TEXT_HEIGHT, C.FONT)
        self.start_button = B.Button(C.START_X - C.START_OFFSET_X, C.START_Y + C.START_OFFSET_Y, C.START_WIDTH, C.START_HEIGHT, C.START_TEXT,
                                          C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.sign_out_button = B.Button(C.SIGN_OUT_X, C.SIGN_OUT_Y, C.SIGN_OUT_WIDTH, C.SIGN_OUT_HEIGHT,
                                        C.SIGN_OUT_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)

        # Create the board object
        self.board = BG.BattleScreen()

    def draw_account(self):
        """Draws the user information on the screen and the buttons"""
        self.screen.fill(C.BLUE)
        self.screen.blit(self.title, (C.ACCOUNT_MESSAGE_X, C.ACCOUNT_MESSAGE_Y))
        self.screen.blit(self.text_username_label, (C.USERNAME_X, C.USERNAME_Y))
        self.screen.blit(self.username, (C.USERNAME_X + C.USER_PASS_OFFSET, C.USERNAME_Y))
        self.screen.blit(self.total_wins_label, (C.USERNAME_X, C.USERNAME_Y + C.ACCOUNT_PASSWORD_OFFSET))
        self.screen.blit(self.total_losses_label, (C.USERNAME_X + C.USER_PASS_OFFSET,
                                                   C.USERNAME_Y + C.ACCOUNT_PASSWORD_OFFSET))
        self.reset_password_textbox.draw(self.screen)
        # Redraw the buttons; Needed for hover cover
        self.load_game_button.draw(self.screen)
        self.reset_pass_button.draw(self.screen)
        self.start_button.draw(self.screen)
        self.sign_out_button.draw(self.screen)
        pygame.display.flip()

    def load_game(self, save_name):
        """Load the game from a saved file"""
        ship_names = ["airecraft_carrier", "battleship", "cruiser", "submarine", "destroyer"]
        with open(C.GAME_FOLDER + save_name, "r") as file:
            data = json.load(file)
            self.board.grid.grid = data["player_grid"]
            self.board.opponent_grid.grid = data["opponent_grid"]
            if data["current_turn"] == "Player 1":
                self.board.player_turn = data["current_turn"]
            else:
                self.board.player_turn = not data["current_turn"]
            self.update_ships(data)
            self.board.ship_count = 5
            self.board.startedBoard = True
            self.board.placeShips = False
            self.board.loaded_game = True
            self.board.rotate_button.disabled = True
            self.board.message = "Game loaded successfully"
            self.screen.fill(C.LIGHTER_BLUE_COLOR)
            self.running = False    # Stop the account screen
            self.board.startDisplay(self.board.main_loop)       # Start the game screen

    def update_ships(self, data):
        """Update the ships with the data from the saved game"""
        count = 0
        for key in data.keys():
            if key.startswith("my_") or key.startswith("opp_"):  # To avoid the grid data and current turn data
                if count == 5:
                    count = 0   # Reset the count to 0 after going through the first 5 ships
                if key.startswith("my_"):  # Handles players ships only
                    ship_list = self.board.ships    # Assign the player ships list
                else:
                    ship_list = self.board.opponent_ships   # Assign the opponent ships list
                ship = ship_list[count]  # Iterate through the ship list
                ship.head_coordinate = data[key][0]  # Add the head coordinates to each ship
                ship.rotated = data[key][1]  # Add the direction of the ship
                ship.sunken = data[key][2]  # Add the sunken status of the ship
                ship.hit_count = data[key][3]  # Add the hit count of the ship
                count += 1


    def main_loop(self):
        """This runs the main loop for the account screen"""
        while self.running:
            self.draw_account()     # Draw the account screen; Needed to refresh the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle the reset password text field events
                self.reset_password_textbox.handle_event(event)
                # Change the buttons to hover color if hovered with cursor
                if self.load_game_button.is_hovered():
                    self.load_game_button.color = C.HOVER_COLOR
                else:
                    self.load_game_button.color = C.GREY
                if self.reset_pass_button.is_hovered():
                    self.reset_pass_button.color = C.HOVER_COLOR
                else:
                    self.reset_pass_button.color = C.GREY
                if self.start_button.is_hovered():
                    self.start_button.color = C.HOVER_COLOR
                else:
                    self.start_button.color = C.GREY
                if self.sign_out_button.is_hovered():
                    self.sign_out_button.color = C.HOVER_COLOR
                else:
                    self.sign_out_button.color = C.GREY
                # Handle when the buttons are clicked
                if self.load_game_button.is_clicked():
                    self.running = False
                    self.load_game("my_new_game.json")
                # Handle resetting the password
                if self.reset_pass_button.is_clicked():
                    self.user.reset_password(self.reset_password_textbox.text)
                    # Clear the text field after resetting
                    self.reset_password_textbox.text = ""
                    self.reset_password_textbox.txt_surface = self.reset_password_textbox.font.render(
                        self.reset_password_textbox.text, True, self.reset_password_textbox.color)
                    # Display the password reset confirmation message
                    self.title = C.FONT.render("Password reset successfully", True, C.WHITE_FONT_COLOR)
                if self.start_button.is_clicked():
                    self.board.username = self.user.username
                    self.board.signed_in = True
                    self.running = False
                    self.screen.fill(C.LIGHTER_BLUE_COLOR)
                    self.board.startDisplay(self.board.main_loop)
                if self.sign_out_button.is_clicked():
                    self.running = False
                    sign_in = SI.SignInDisplay()
                    sign_in.startDisplay(sign_in.main_loop)
                pygame.display.flip()


if __name__ == "__main__":
    person = Account.Account("Agatha", 10)
    account_display = AccountDisplay(person)
    account_display.startDisplay(account_display.main_loop)
