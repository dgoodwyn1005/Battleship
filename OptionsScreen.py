import os
import json
import pygame.display
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD
import Ships
import SoundManager as SM
from textbox import TextBox

class Options_Screen(D.Display):

    play_music = True
    play_sound_effects = True
    # Initialize the screen and the parameters are used to save the game. None is default so that Main_Menu cannot
    # save a game that has not began
    def __init__(self, player_grid = None, opponent_grid = None, current_turn = None, player_ships: [Ships.Ships] = None,
                 opponent_ships: [Ships.Ships] = None, signed_in=False, username=None):
        super().__init__(screenName= C.OPTIONS_CAPTION, background= C.BLUE)
        self.sounds = SM.Sound()
        self.music_button = B.Button(C.MUSIC_X, C.MUSIC_Y, C.MUSIC_WIDTH, C.MUSIC_HEIGHT, C.MUSIC_TEXT,
                                     C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.sounds_button = B.Button(C.SOUNDS_X, C.SOUNDS_Y, C.SOUNDS_WIDTH, C.SOUNDS_HEIGHT, C.SOUNDS_TEXT,
                                      C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.back_button = B.Button(C.BACK_X, C.BACK_Y, C.BACK_WIDTH_HEIGHT, C.BACK_WIDTH_HEIGHT, C.BACK_TEXT,
                                    C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        self.game_display = GD.GameDisplay(self.screen)
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

        # Draw the message label on the screen
        self.screen.blit(self.message_label, (C.FILENAME_X, C.FILENAME_Y - C.SAVE_MESSAGE_OFFSET))
        # Draw the settings on the screen
        self.game_display.draw_settings("On" if SM.Sound.play_music else "Off",
                                        "On" if SM.Sound.play_sound_effects else "Off")

    def toggle_music(self):
        """Toggle the music on and off"""
        self.sounds.toggle_music()     # Toggle the music using the SoundManager method
        if self.sounds.play_music:      # If music is enabled, play the menu song
            self.sounds.play_song("menu")
        else:                        # Otherwise, stop the menu song
            self.sounds.stop_song("menu")
        self.draw_buttons_and_settings()    # Redraw the buttons and settings to show the updated On and Off options

    def toggle_sound_effects(self):
        """Toggle the sound effects on and off"""
        self.sounds.toggle_sounds()     # Toggle the sound effects using the SoundManager method
        self.draw_buttons_and_settings()    # Redraw the buttons and settings to show the updated On and Off options

    def go_back(self):
        """When the back button is clicked, go back to the main menu"""
        self.running = False

    def save_game(self, save_name):
        """Save the game settings to a file"""
        if not os.path.exists(C.GAME_FOLDER + self.username):   # Check if the user has a folder
            os.makedirs(C.GAME_FOLDER + self.username)  # Create a folder for the user if there isn't one
        save_location = C.GAME_FOLDER + self.username + "/"  # Set the save location to the user's folder
        # Ensure that all ships have been placed and the player is signed in before attempting to save the game
        if self.player_grid != None and self.player_ships[4].head_coordinate != (-1, -1) and self.signed_in != False:
            with open(save_location + save_name, "w") as file:
                data = {"player_grid": self.player_grid, "opponent_grid": self.opponent_grid,
                        "current_turn": self.current_turn}
                # Save the head coordinates of the ships so that the images can be reloaded at the correct positions
                for ship in self.player_ships:      # Save the player's ships together
                    data["my_" + ship.name] = (ship.head_coordinate, ship.rotated, ship.sunken, ship.hit_count)
                for ship in self.opponent_ships:    # Save the opponent's ships together
                    data["opp_" + ship.name] = (ship.head_coordinate, ship.rotated, ship.sunken, ship.hit_count)
                json.dump(data, file, indent=4)     # Dump the data to the file

    def check_valid_name(self, name: str):
        """Check if the enter file name is valid"""
        if name == "":
            self.message_label = C.FONT.render("Please enter a file name", True, C.RED)
            return False
        elif name.find(".") != -1:  # Check if the file name contains a '.'; otherwise .find() returns -1
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
                # Mouse button ensures only one click is registered
                if self.music_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.sounds.play_sound("click")
                    self.toggle_music()
                elif self.sounds_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.sounds.play_sound("click")
                    self.toggle_sound_effects()
                elif self.save_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.sounds.play_sound("click")
                    # Check if the entered name is acceptable
                    filename = self.filename_textbox.text
                    if not self.signed_in:
                        self.message_label = C.FONT.render("You must be signed in to save a game", True, C.RED)
                    elif self.player_ships[4].head_coordinate == (-1, -1):
                        self.message_label = C.FONT.render("You must place all ships to save a game", True, C.RED)
                    elif self.check_valid_name(filename):
                        self.save_game(filename + ".json")
                        self.message_label = C.FONT.render("Game saved!", True, C.WHITE_FONT_COLOR)
                    else:
                        self.message_label = C.FONT.render("Invalid file name", True, C.RED)
                elif self.back_button.is_clicked() and event.type == pygame.MOUSEBUTTONDOWN:
                    self.sounds.play_sound("click")
                    self.go_back()
            self.draw_buttons_and_settings()
            pygame.display.flip()


if __name__ == "__main__":
    screen = Options_Screen()
    screen.startDisplay(screen.main_loop)
