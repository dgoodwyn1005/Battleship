import json
import pygame.display
import Board as BG
import Display as D
import Constants as C
import Button as B
import GameDisplay as GD
import OptionsScreen as OS
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
        self.load_game_button = B.Button(C.LOAD_X, C.LOAD_Y, C.LOAD_WIDTH, C.LOAD_HEIGHT, C.LOAD_TEXT,
                                         C.FONT, C.GREY, C.WHITE_FONT_COLOR)
        
        # Initialize text box
        self.font = pygame.font.Font(None, 32)
        self.textbox = TextBox(C.TEXTBOX_X, C.TEXTBOX_Y, C.TEXTBOX_WIDTH, C.TEXTBOX_HEIGHT, C.FONT)
        self.username = "Player 1"
        self.game_display = GD.GameDisplay(self.screen)
        self.draw_buttons_and_text()

        # Create board object
        self.board = BG.BattleScreen()


    def draw_buttons_and_text(self):
        # self.screen.fill(C.BLUE)

        # Detect mouse hover and change button colors accordingly
        if self.start_button.is_hovered():
            self.start_button.color = C.HOVER_COLOR
        else:
            self.start_button.color = C.GREY

        if self.options_button.is_hovered():
            self.options_button.color = C.HOVER_COLOR
        else:
            self.options_button.color = C.GREY

        if self.quit_button.is_hovered():
            self.quit_button.color = C.HOVER_COLOR
        else:
            self.quit_button.color = C.GREY

        if self.load_game_button.is_hovered():
            self.load_game_button.color = C.HOVER_COLOR
        else:
            self.load_game_button.color = C.GREY

        # Draw buttons
        self.start_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.load_game_button.draw(self.screen)

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

    def load_game(self, save_name):
        """Load the game from a saved file"""
        with open(C.GAME_FOLDER + save_name, "r") as file:
            data = json.load(file)
            self.board.grid.grid = data["player_grid"]
            self.board.opponent_grid.grid = data["opponent_grid"]
            if data["current_turn"] == "Player 1":
                self.board.player_turn = data["current_turn"]
            else:
                self.board.player_turn = not data["current_turn"]
            self.board.ship_count = 5
            self.board.startedBoard = True
            self.board.placeShips = False
            self.board.loaded_game = True
            self.board.rotate_button.disabled = True
            self.board.message = "Game loaded successfully"
            self.screen.fill(C.LIGHTER_BLUE_COLOR)
            self.board.startDisplay(self.board.main_loop)




    def main_loop(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle text box events
                self.textbox.handle_event(event)

                # Update the username if Enter is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.username = self.textbox.text

                # Handle button clicks
                if self.start_button.is_clicked():
                    self.username = self.textbox.text if self.textbox.text else self.username
                    self.running = False
                    self.screen.fill(C.LIGHTER_BLUE_COLOR)
                    self.board.startDisplay(self.board.main_loop)
                    # battle_screen = BG.BattleScreen(username=self.username)
                    # battle_screen.startDisplay(battle_screen.main_loop)

                if self.options_button.is_clicked():
                  # Transition to options screen
                    screen = OS.Options_Screen()
                    screen.startDisplay(screen.main_loop)

                if self.quit_button.is_clicked():
                    print("Quit Game")
                    self.running = False
                if self.load_game_button.is_clicked():
                    self.running = False
                    self.load_game("save.json")

               

            self.screen.fill(C.BLUE)
            self.draw_buttons_and_text()


if __name__ == "__main__":
    screen = Main_Menu()
    screen.startDisplay(screen.main_loop)
