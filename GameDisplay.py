
import Constants as C
import pygame

class GameDisplay(object):

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 25)
    
    # Draws player names in the corners
    def draw_names(self, player1, player2):
        player_text = self.font.render(f"Player: {player1}", True, C.WHITE_FONT_COLOR)
        opponent_text = self.font.render(f"Opponent: {player2}", True, C.WHITE_FONT_COLOR)
        self.screen.blit(player_text, (10, 10))  # top left corner
        self.screen.blit(opponent_text, (self.screen.get_width() - opponent_text.get_width() - 10, 10)) # top right corner
    
    # Draw the turn indicator in the center
    def draw_turn_indicator(self, current_player):

        # Define the rectangle area to clear the previous turn message
        turn_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() - 35, 200, 30)
        self.screen.fill(C.LIGHTER_BLUE_COLOR, turn_rect)  # Clear with background color

        turn_text = self.font.render(f"Turn: {current_player}", True, C.WHITE_FONT_COLOR)
        text_rect = turn_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 25))
        self.screen.blit(turn_text, text_rect)

# Draw the message in the center
    def draw_message(self, message):
        # Clear previous message by drawing a rectangle over it
        message_rect = pygame.Rect(self.screen.get_width() // 3, self.screen.get_height() // 15 - 10, self.screen.get_width() // 3, 30)
        self.screen.fill(C.LIGHTER_BLUE_COLOR, message_rect)

        # Draw the new message
        message_text = self.font.render(message, True, C.WHITE_FONT_COLOR)
        text_rect = message_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 15))
        self.screen.blit(message_text, text_rect)

    # Draw the settings buttons on the options screen
    def draw_settings(self, music, sounds):
        music_text = self.font.render(f"Music: {music}", True, C.WHITE_FONT_COLOR)
        sounds_text = self.font.render(f"Sounds: {sounds}", True, C.WHITE_FONT_COLOR)
        self.screen.blit(music_text, (self.screen.get_width() // 2 - 35, 50))
        self.screen.blit(sounds_text, (self.screen.get_width() // 2 - 35, 30))
