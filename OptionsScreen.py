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
        self.music_button = B.Button(C.MUSIC_X, C.MUSIC_Y, C.MUSIC_WIDTH_HEIGHT, C.MUSIC_WIDTH_HEIGHT, C.MUSIC_TEXT,
                                     C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.sounds_button = B.Button(C.SOUNDS_X, C.SOUNDS_Y, C.SOUNDS_WIDTH_HEIGHT, C.SOUNDS_WIDTH_HEIGHT, C.SOUNDS_TEXT,
                                      C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT,
                                    C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.game_display = GD.GameDisplay(self.screen)
        # Draw buttons
        self.music_button.draw(self.screen)
        self.sounds_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.game_display.draw_settings(self.play_music, self.play_sound_effects)


    def toggle_music(self):
        self.play_music = not self.play_music


    def toggle_sound_effects(self):
        self.play_sound_effects = not self.play_sound_effects

    def go_back(self):
        self.running = False
        print("Go back")


    def main_loop(self):
        if self.music_button.is_clicked():
            self.toggle_music()
            print("Music: ", self.play_music)
        elif self.sounds_button.is_clicked():
            self.toggle_sound_effects()
            print("Sound Effects: ", self.play_sound_effects)
        elif self.back_button.is_clicked():
            self.go_back()


screen = Options_Screen()
D.Display.startDisplay(screen, screen.main_loop)

