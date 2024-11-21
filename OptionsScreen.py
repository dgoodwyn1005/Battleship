import json
import pygame.display
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD
import Ships
from textbox import TextBox



class Options_Screen(D.Display):

    play_music = True
    play_sound_effects = True
    # Initialize the screen and the parameters are used to save the game. None is default so that Main_Menu cannot
    # save a game that has not began
    def __init__(self, player_grid = None, opponent_grid = None, current_turn = None, player_ships: [Ships.Ships] = None,
                 opponent_ships: [Ships.Ships] = None, signed_in = False, username = None):
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
        self.filename_textbox = TextBox(C.FILENAME_X, C.FILENAME_Y, C.FILENAME_WIDTH, C.FILENAME_HEIGHT, C.FONT)
        self.message_label = C.FONT.render("", True, C.WHITE_FONT_COLOR)
        # Data used to save the game
        self.player_grid = player_grid
        self.opponent_grid = opponent_grid
        self.current_turn = current_turn
        self.player_ships = player_ships
        self.opponent_ships = opponent_ships
        self.signed_in = signed_in
        self.username = username


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
        self.filename_textbox.draw(self.screen)
        self.screen.blit(self.message_label, (C.FILENAME_X, C.FILENAME_Y - C.SAVE_MESSAGE_OFFSET))

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
                json.dump(data, file, indent=4)

    def check_valid_name(self, name: str):
        """Check if the enter file name is valid"""
        if name == "":
            self.message_label = C.FONT.render("Please enter a file name", True, C.RED)
            return False
        elif name.find(".") != -1:  # Check if the file name contains a '.'; otherise .find() returns -1
            self.message_label = C.FONT.render("File name cannot contain '.'", True, C.RED)
            return False
        elif name.find("/") != -1:  # Check if the file name contains a '/'
            self.message_label = C.FONT.render("File name cannot contain '/'", True, C.RED)
            return False
        elif name.find("\\") != -1:
            self.message_label = C.FONT.render("File name cannot contain '\\'", True, C.RED)
            return False
        elif name.find(":") != -1:
            self.message_label = C.FONT.render("File name cannot contain ':'", True, C.RED)
            return False
        return True

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                self.draw_buttons_and_settings()  # Draw the buttons and settings
                if event.type == pygame.QUIT:
                    self.running = False
                self.filename_textbox.handle_event(event)
                # Mousebutton ensures only one click is registered
                if self.music_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_music()
                elif self.sounds_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.toggle_sound_effects()
                elif self.save_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the entered name is acceptable
                    filename = self.filename_textbox.text
                    if not self.signed_in:
                        self.message_label = C.FONT.render("You must be signed in to save a game", True, C.RED)
                    elif self.check_valid_name(filename):
                        self.save_game(filename + ".json")
                        self.message_label = C.FONT.render("Game saved!", True, C.WHITE_FONT_COLOR)
                        print("Settings saved clicked")
                    else:
                        self.message_label = C.FONT.render("Invalid file name", True, C.RED)
                elif self.back_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.go_back()
            self.draw_buttons_and_settings()


if __name__ == "__main__":
    screen = Options_Screen()
    screen.startDisplay(screen.main_loop)
