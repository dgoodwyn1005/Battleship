import json

import pygame.display
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD

class Options_Screen(D.Display):

    play_music = True
    play_sound_effects = True
    # Initialize the screen and the parameters are used to save the game. None is default so that Main_Menu cannot
    # save a game that has not began
    def __init__(self, player_grid = None, opponent_grid = None, current_turn = None, player_ships = None,
                 opponent_ships = None):
        super().__init__(screenName= C.OPTIONS_CAPTION, background= C.BLUE)
        self.music_button = B.Button(C.MUSIC_X, C.MUSIC_Y, C.MUSIC_WIDTH, C.MUSIC_HEIGHT, C.MUSIC_TEXT,
                                     C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.sounds_button = B.Button(C.SOUNDS_X, C.SOUNDS_Y, C.SOUNDS_WIDTH, C.SOUNDS_HEIGHT, C.SOUNDS_TEXT,
                                      C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT,
                                    C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.game_display = GD.GameDisplay(self.screen)
        self.explosion_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/explosion_sound.wav")
        self.water_sound = pygame.mixer.Sound(C.AUDIO_FOLDER + "/water_splash_sound.wav")
        self.save_button = B.Button(C.SAVE_X, C.SAVE_Y, C.SAVE_WIDTH, C.SAVE_HEIGHT, C.SAVE_TEXT, C.FONT, C.GREY,
                                    C.WHITE_FONT_COLOR)
        # Data used to save the game
        self.player_grid = player_grid
        self.opponent_grid = opponent_grid
        self.current_turn = current_turn
        self.player_ships = player_ships
        self.opponent_ships = opponent_ships
        self.sounds = SM.Sound(100, 100)

    def draw_buttons_and_settings(self):
        # Draw buttons
        self.screen.fill(C.BLUE)
        # Check for hover and change music button colors
        if self.music_button.is_hovered():
            self.music_button.color = C.HOVER_COLOR
        else:
            self.music_button.color = C.GREY
        # Check for hover and change sounds button colors
        if self.sounds_button.is_hovered():
            self.sounds_button.color = C.HOVER_COLOR
        else:
            self.sounds_button.color = C.GREY
        # Check for hover and change back button colors
        if self.back_button.is_hovered():
            self.back_button.color = C.HOVER_COLOR
        else:
            self.back_button.color = C.GREY
        # Check for hover and change save button colors
        if self.save_button.is_hovered():
            self.save_button.color = C.HOVER_COLOR
        else:
            self.save_button.color = C.GREY
        self.music_button.draw(self.screen)
        self.sounds_button.draw(self.screen)
        self.save_button.draw(self.screen)
        self.back_button.draw(self.screen)

        self.game_display.draw_settings("On" if self.sounds.play_music else "Off",
                                        "On" if self.sounds.play_sound_effects else "Off")



    def toggle_music(self):
        """Toggle the music on and off"""
        self.sounds.toggle_music(not self.sounds.play_music)
        self.draw_buttons_and_settings()

    def toggle_sound_effects(self):
        """Toggle the sound effects on and off"""
        self.sounds.toggle_sounds(not self.sounds.play_sound_effects)
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

    def save_game(self, save_name):
        """Save the game settings to a file"""
        if (self.player_grid != None and self.opponent_grid != None and len(self.player_ships) == 5
                and len(self.opponent_ships) == 5):
            with open(C.GAME_FOLDER + save_name, "w") as file:
                data = {}
                data["player_grid"] = self.player_grid
                data["opponent_grid"] = self.opponent_grid
                data["current_turn"] = self.current_turn
                for ship in self.player_ships:
                    data[ship.name] = ship.head_coordinate
                data["player_ship_coordinates"] = self.player_ships.head_coordinate
                data["opponent_ships"] = self.opponent_ships
                json.dump(data, file)

    def main_loop(self):
        self.draw_buttons_and_settings()  # Draw the buttons and settings
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Mousebutton ensures only one click is registered
                if self.music_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_music()
                elif self.sounds_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_sound_effects()
                elif self.save_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.save_game("save.json")
                    print("Settings saved clicked")
                elif self.back_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.go_back()
            self.draw_buttons_and_settings()

if __name__ == "__main__":
    screen = Options_Screen()
    screen.startDisplay(screen.main_loop)
