import Display as D
import pygame
import Constants as C
import Button as B
import Account
import Board as BG
from textbox import TextBox
import SignIn as SI
import LoadGameDisplay as LGD
import SoundManager as SM


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
        self.start_button = B.Button(C.START_X - C.START_OFFSET_X, C.START_Y + C.START_OFFSET_Y, C.START_WIDTH,
                                     C.START_HEIGHT, C.START_TEXT,
                                     C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.sign_out_button = B.Button(C.SIGN_OUT_X, C.SIGN_OUT_Y, C.SIGN_OUT_WIDTH, C.SIGN_OUT_HEIGHT,
                                        C.SIGN_OUT_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        # Create the board object
        self.board = BG.BattleScreen(user=self.user)
        self.sounds = SM.Sound()

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

    def load_game(self):
        load_screen = LGD.LoadGameDisplay(self.user.username, self.user)
        load_screen.startDisplay(load_screen.main_loop)

    def main_loop(self):
        """This runs the main loop for the account screen"""
        # Create a list of the screen to iterate through
        button_list = [self.load_game_button, self.reset_pass_button, self.start_button, self.sign_out_button]
        while self.running:
            self.draw_account()     # Draw the account screen; Needed to refresh the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle the reset password text field events
                self.reset_password_textbox.handle_event(event)

                # Change the buttons to hover color if hovered with cursor
                for button in button_list:
                    if button.is_hovered():  # If any button is hovered, change the color to the hover cover
                        button.color = C.HOVER_COLOR
                    else:
                        button.color = C.GREY
                    if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                        self.sounds.play_sound("click")  # Play the click sound
                        # Handle when the buttons are clicked
                        if button == self.load_game_button:
                            self.running = False
                            self.load_game()
                        # Handle resetting the password
                        if button == self.reset_pass_button and self.reset_password_textbox.text != "":
                            self.user.reset_password(self.reset_password_textbox.text)
                            # Clear the text field after resetting
                            self.reset_password_textbox.text = ""
                            self.reset_password_textbox.txt_surface = self.reset_password_textbox.font.render(
                                self.reset_password_textbox.text, True, self.reset_password_textbox.color)
                            # Display the password reset confirmation message
                            self.title = C.FONT.render("Password reset successfully", True, C.WHITE_FONT_COLOR)
                        # Handle empty text box for resetting password
                        elif button == self.reset_pass_button and self.reset_password_textbox.text == "":
                            self.title = C.FONT.render("Please enter a new password", True, C.RED)
                        # Handle the start button
                        if button == self.start_button:
                            # Set the username and signed_in attributes of the board object so that user can save
                            # the game
                            self.board.username = self.user.username
                            self.board.signed_in = True
                            self.running = False
                            self.screen.fill(C.LIGHTER_BLUE_COLOR)
                            self.board.startDisplay(self.board.main_loop)
                        # Handle the sign-out button
                        if button == self.sign_out_button:
                            self.running = False
                            sign_in = SI.SignInDisplay()
                            sign_in.startDisplay(sign_in.main_loop)
                pygame.display.flip()


if __name__ == "__main__":
    person = Account.Account("Agatha", 10)
    account_display = AccountDisplay(person)
    account_display.startDisplay(account_display.main_loop)
