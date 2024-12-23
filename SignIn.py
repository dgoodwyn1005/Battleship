import Display as D
import Constants as C
import Button as B
import pygame
from textbox import TextBox
import Account as A
import AccountDisplay as AD
import SoundManager as SM


class SignInDisplay(D.Display):

    def __init__(self):
        super().__init__(screenName= C.ACCOUNT_CAPTION, background= C.BLUE)
        self.username = ""
        self.password = ""
        self.username_text = TextBox(C.USERNAME_X, C.USERNAME_Y, C.USERNAME_WIDTH, C.USERNAME_HEIGHT, C.FONT)
        self.password_text = TextBox(C.USERNAME_X, C.USERNAME_Y + C.ACCOUNT_PASSWORD_OFFSET,
                                     C.USERNAME_WIDTH, C.USERNAME_HEIGHT, C.FONT, is_password=True)
        self.sign_in_button = B.Button(C.SIGN_IN_X, C.SIGN_IN_Y, C.SIGN_IN_WIDTH, C.SIGN_IN_HEIGHT, C.SIGN_IN_TEXT,
                                       C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.account_label = C.FONT.render(C.ACCOUNT_TEXT, True, C.WHITE_FONT_COLOR)  # Create the account label
        self.register_button = B.Button(C.REGISTER_X, C.REGISTER_Y, C.REGISTER_WIDTH, C.REGISTER_HEIGHT,
                                        C.REGISTER_TEXT, C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT, C.FONT,
                                    C.GREY, C.WHITE_FONT_COLOR)
        self.sounds = SM.Sound()



    def draw_buttons_and_text(self):
        self.screen.fill(C.BLUE)  # Fill the screen with the background color, so it doesn't show the previous screen
        # Draw the screen buttons
        self.username_text.draw(self.screen)
        self.password_text.draw(self.screen)
        self.sign_in_button.draw(self.screen)
        self.register_button.draw(self.screen)
        self.back_button.draw(self.screen)
        # The labels that are drawn on the screen
        username_label = C.FONT.render(C.USERNAME_TEXT, True, C.WHITE_FONT_COLOR)  # Create the username label
        password_label = C.FONT.render(C.PASSWORD_TEXT, True, C.WHITE_FONT_COLOR)  # Create the password label
        # Draw the account message label
        self.screen.blit(self.account_label, (C.ACCOUNT_MESSAGE_X, C.ACCOUNT_MESSAGE_Y))
        # Draw the username label
        self.screen.blit(username_label, (C.USERNAME_X - C.USER_PASS_OFFSET, C.USERNAME_Y))
        # Draw the password label
        self.screen.blit(password_label, (C.USERNAME_X - C.USER_PASS_OFFSET, C.USERNAME_Y + C.ACCOUNT_PASSWORD_OFFSET))
        # Check for hover and change sign in button colors
        if self.sign_in_button.is_hovered():
            self.sign_in_button.color = C.HOVER_COLOR
        else:
            self.sign_in_button.color = C.GREY
        self.sign_in_button.draw(self.screen)
        if self.register_button.is_hovered():
            self.register_button.color = C.HOVER_COLOR
        else:
            self.register_button.color = C.GREY
        pygame.display.flip()

    def handle_event(self, event):
        self.username_text.handle_event(event)
        self.password_text.handle_event(event)
        self.sign_in_button.draw(self.screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.username = self.username_text.text
            self.password = self.password_text.text
            self.username_text.txt_surface = self.username_text.font.render(self.username_text.text, True, self.username_text.color)
            self.password_text.txt_surface = self.password_text.font.render(self.password_text.text, True, self.password_text.color)
            if self.sign_in_button.is_hovered():
                self.sign_in_button.color = C.HOVER_COLOR
            else:
                self.sign_in_button.color = C.GREY
        self.draw_buttons_and_text()

    def main_loop(self):
        buttons = [self.sign_in_button, self.register_button, self.back_button]
        self.draw_buttons_and_text()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)
                for button in buttons:
                    if button.is_hovered():
                        button.color = C.HOVER_COLOR
                    else:
                        button.color = C.GREY
                    if button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                        self.sounds.play_sound("click")
                        if button == self.sign_in_button and event.type == pygame.MOUSEBUTTONDOWN:
                            # Verify that the accounts exists
                            verify = A.Account.log_in(self.username_text.text, self.password_text.text)
                            if verify:
                                user = A.Account(self.username_text.text, self.password_text.text)
                                self.account_label = C.FONT.render("Account verified", True, C.WHITE_FONT_COLOR)
                                self.running = False
                                user_details = AD.AccountDisplay(user)
                                user_details.startDisplay(user_details.main_loop)
                            else:
                                self.account_label = C.FONT.render("Account not verified", True, C.WHITE_FONT_COLOR)
                        if button == self.register_button and event.type == pygame.MOUSEBUTTONDOWN:
                            username = self.username_text.text
                            password = self.password_text.text
                            if username == "" or password == "":
                                self.account_label = C.FONT.render("Please enter a username and password", True, C.WHITE_FONT_COLOR)
                            else:
                                verify = A.Account.log_in(username, password)
                                if not verify:
                                    new_user = A.Account(username, password)
                                    new_user.create_account()
                                    self.account_label = C.FONT.render("Account created", True, C.WHITE_FONT_COLOR)
                                else:
                                    self.account_label = C.FONT.render("Account already exists", True, C.WHITE_FONT_COLOR)
                        if button == self.back_button and event.type == pygame.MOUSEBUTTONDOWN:
                            self.running = False
                            self.screen.fill(C.LIGHTER_BLUE_COLOR)
        self.draw_buttons_and_text()


if __name__ == '__main__':
    account = SignInDisplay()
    account.startDisplay(account.main_loop)
