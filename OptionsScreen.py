import pygame.display
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD

class Options_Screen(D.Display):

    play_music = True
    play_sound_effects = True

    def __init__(self):
        super().__init__(screenName= C.OPTIONS_CAPTION, background= C.BLUE)
        self.music_button = B.Button(C.MUSIC_X, C.MUSIC_Y, C.MUSIC_WIDTH, C.MUSIC_HEIGHT, C.MUSIC_TEXT,
                                     C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.sounds_button = B.Button(C.SOUNDS_X, C.SOUNDS_Y, C.SOUNDS_WIDTH, C.SOUNDS_HEIGHT, C.SOUNDS_TEXT,
                                      C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT,
                                    C.font, C.GREY, C.WHITE_FONT_COLOR)
        self.game_display = GD.GameDisplay(self.screen)
        self.explosion_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/explosion_sound.wav")
        self.water_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/water_splash_sound.wav")



    def draw_buttons_and_settings(self):
        # Draw buttons
        self.screen.fill(C.BLUE)
        # Check for hover and change button colors
        if self.music_button.is_hovered():
            self.music_button.color = C.HOVER_COLOR
        else:
            self.music_button.color = C.GREY

        if self.sounds_button.is_hovered():
            self.sounds_button.color = C.HOVER_COLOR
        else:
            self.sounds_button.color = C.GREY

        if self.back_button.is_hovered():
            self.back_button.color = C.HOVER_COLOR
        else:
            self.back_button.color = C.GREY
        self.music_button.draw(self.screen)
        self.sounds_button.draw(self.screen)
        self.back_button.draw(self.screen)

        self.game_display.draw_settings("On" if Options_Screen.play_music else "Off",
                                        "On" if Options_Screen.play_sound_effects else "Off")
        pygame.display.flip()


    def toggle_music(self):
        """Toggle the music on and off"""
        Options_Screen.play_music = not Options_Screen.play_music
        self.draw_buttons_and_settings()


    def toggle_sound_effects(self):
        """Toggle the sound effects on and off"""
        Options_Screen.play_sound_effects = not Options_Screen.play_sound_effects
        self.draw_buttons_and_settings()

    def go_back(self):
        """When the back button is clicked, go back to the main menu"""
        self.running = False

    def play_explosion_sound(self):
        if Options_Screen.play_sound_effects:
            self.explosion_sound.play()

    def play_water_sound(self):
        if Options_Screen.play_sound_effects:
            self.water_sound.play()


    def main_loop(self):
        self.draw_buttons_and_settings() # Draw the buttons and settings
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Mousebutton ensures only one click is registered
                if self.music_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_music()
                elif self.sounds_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_sound_effects()
                elif self.back_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.go_back()
            self.draw_buttons_and_settings()

if __name__ == "__main__":
    screen = Options_Screen()
    screen.startDisplay(screen.main_loop)
