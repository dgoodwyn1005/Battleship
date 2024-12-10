import pygame.display
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD
import Board as BG
import OptionsScreen as OS
import SignIn as SI
import SoundManager as SM
from textbox import TextBox

class Main_Menu(D.Display):
    def __init__(self):
        super().__init__(screenName= C.MENU_CAPTION, background= C.BLUE)
        self.start_button = B.Button(C.START_X, C.START_Y, C.START_WIDTH, C.START_HEIGHT, C.START_TEXT,
                                     C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.options_button = B.Button(C.OPTIONS_X, C.OPTIONS_Y, C.OPTIONS_WIDTH, C.OPTIONS_HEIGHT, C.OPTIONS_TEXT,
                                       C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.quit_button = B.Button(C.QUIT_X, C.QUIT_Y, C.QUIT_WIDTH, C.QUIT_HEIGHT, C.QUIT_TEXT,
                                    C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.account_button = B.Button(C.ACCOUNT_X, C.ACCOUNT_Y, C.ACCOUNT_WIDTH, C.ACCOUNT_HEIGHT, C.ACCOUNT_B_TEXT,
                                       C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        # Initialize text box
        self.font = pygame.font.Font(None, 32)
        self.textbox = TextBox(C.TEXTBOX_X, C.TEXTBOX_Y, C.TEXTBOX_WIDTH, C.TEXTBOX_HEIGHT, C.FONT)
        self.username = "Player 1"
        self.game_display = GD.GameDisplay(self.screen)
        self.draw_buttons_and_text()

        self.sounds = SM.Sound()

    def draw_buttons_and_text(self):
        """Draws the buttons and text on the screen"""
        # self.screen.fill(C.BLUE)

        # Detect mouse hover and change button colors accordingly
        if self.start_button.is_hovered():
            self.start_button.color = C.HOVER_COLOR
        else:
            self.start_button.color = C.GREY
        # Check for hover and change options button colors
        if self.options_button.is_hovered():
            self.options_button.color = C.HOVER_COLOR
        else:
            self.options_button.color = C.GREY
        # Check for hover and change quit button colors
        if self.quit_button.is_hovered():
            self.quit_button.color = C.HOVER_COLOR
        else:
            self.quit_button.color = C.GREY
        # Check for hover and change account button colors
        if self.account_button.is_hovered():
            self.account_button.color = C.HOVER_COLOR
        else:
            self.account_button.color = C.GREY

        # Draw buttons
        self.start_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.account_button.draw(self.screen)

        # Rendering main menu title text
        menu_font = pygame.font.SysFont(None, 25)
        rendered_text = menu_font.render(C.MENU_TEXT, True, C.WHITE_FONT_COLOR)
        text_rect = rendered_text.get_rect(center=(C.TEXT_X, C.TEXT_Y))
        self.screen.blit(rendered_text, text_rect)

        # Draw "Enter Username" label above the text box
        username_label = self.font.render(C.TEXTBOX_TEXT, True, C.WHITE_FONT_COLOR)
        label_rect = username_label.get_rect(center=(C.TEXTBOX_X + C.TEXTBOX_WIDTH // 2, C.TEXTBOX_Y - 20))
        self.screen.blit(username_label, label_rect)

        # Draw text box
        self.textbox.draw(self.screen)

        pygame.display.flip()

    def main_loop(self):

        self.sounds.play_song("menu")

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle text box events
                self.textbox.handle_event(event)

                # Handle button clicks
                if self.start_button.is_clicked():
                    self.username = self.textbox.text if self.textbox.text else self.username
                    self.running = False
                    self.screen.fill(C.LIGHTER_BLUE_COLOR)
                    # self.board.username = self.username
                    # self.board.startDisplay(self.board.main_loop)
                    battle_screen = BG.BattleScreen(username=self.username)
                    battle_screen.startDisplay(battle_screen.main_loop)
                    self.sounds.play_sound("click")

                if self.options_button.is_clicked():
                    self.sounds.play_sound("click")
                  # Transition to options screen
                    screen = OS.Options_Screen()
                    screen.startDisplay(screen.main_loop)

                if self.account_button.is_clicked():
                    self.sounds.play_sound("click")
                    # Transition to account screen
                    login_screen = SI.SignInDisplay()
                    login_screen.startDisplay(login_screen.main_loop)

                if self.quit_button.is_clicked():
                    self.sounds.play_sound("click")
                    self.sounds.stop_song("menu")
                    self.running = False
            self.screen.fill(C.BLUE)
            self.draw_buttons_and_text()


if __name__ == "__main__":
    screen = Main_Menu()
    screen.startDisplay(screen.main_loop)
