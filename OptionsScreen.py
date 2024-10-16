import pygame.display
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD

class Options_Screen(D.Display):

    def __init__(self):
        super().__init__(screenName= C.OPTIONS_CAPTION, background= C.BLUE)
        self.play_music = False
        self.play_sound_effects = False
        self.music_button = B.Button(C.MUSIC_X, C.MUSIC_Y, C.MUSIC_WIDTH, C.MUSIC_HEIGHT, C.MUSIC_TEXT,
                                     C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.sounds_button = B.Button(C.SOUNDS_X, C.SOUNDS_Y, C.SOUNDS_WIDTH, C.SOUNDS_HEIGHT, C.SOUNDS_TEXT,
                                      C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT,
                                    C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.game_display = GD.GameDisplay(self.screen)
        self.draw_buttons_and_settings()
        self.running = True

    def draw_buttons_and_settings(self):
        # Draw buttons
        self.screen.fill(C.BLUE)
        self.music_button.draw(self.screen)
        self.sounds_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.game_display.draw_settings("On" if self.play_music else "Off", "On" if self.play_sound_effects else "Off")
        pygame.display.flip()


    def toggle_music(self):
        self.play_music = not self.play_music
        self.draw_buttons_and_settings()


    def toggle_sound_effects(self):
        self.play_sound_effects = not self.play_sound_effects
        self.draw_buttons_and_settings()

    def go_back(self):
        self.running = False
        print("Go back")


    def main_loop(self):
        for event in pygame.event.get():
            if self.music_button.is_clicked():
                self.toggle_music()
                print("Music: ", self.play_music)
            elif self.sounds_button.is_clicked():
                self.toggle_sound_effects()
                print("Sound Effects: ", self.play_sound_effects)
            elif self.back_button.is_clicked():
                self.go_back()


# screen = Options_Screen()
# D.Display.startDisplay(screen, screen.main_loop)
