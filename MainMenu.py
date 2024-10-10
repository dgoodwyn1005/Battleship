import pygame.display

import Display as D
import Constants as C
import Button as B
import GameDisplay as GD
import OptionsScreen as OS

class Main_Menu(D.Display):
    def __init__(self):
        super().__init__(screenName= C.MENU_CAPTION, background= C.BLUE)
        self.start_button = B.Button(C.START_X, C.START_Y, C.START_WIDTH, C.START_HEIGHT, C.START_TEXT,
                                     C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.options_button = B.Button(C.OPTIONS_X, C.OPTIONS_Y, C.OPTIONS_WIDTH, C.OPTIONS_HEIGHT, C.OPTIONS_TEXT,
                                       C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.quit_button = B.Button(C.QUIT_X, C.QUIT_Y, C.QUIT_WIDTH, C.QUIT_HEIGHT, C.QUIT_TEXT,
                                    C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.text = C.MENU_TEXT
        self.font = C.MENU_FONT
        self.game_display = GD.GameDisplay(self.screen)
        self.draw_buttons_and_text()

    def draw_buttons_and_text(self):
        self.screen.fill(C.BLUE)
        self.start_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.text = self.font.render(self.text, True, C.WHITE_FONT_COLOR)
        text_rect = self.text.get_rect(center=(C.TEXT_X, C.TEXT_Y))
        self.screen.blit(self.text, text_rect)

        pygame.display.flip()

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.start_button.is_clicked():
                    print("Start Game")  # Transition to game loop
                    running = False
                if self.options_button.is_clicked():
                    print("Options Selected")  # Transition to options screen
                    op_screen = OS.Options_Screen()
                    D.Display.startDisplay(op_screen, op_screen.main_loop)
                if self.quit_button.is_clicked():
                    pygame.quit()
                    exit()
