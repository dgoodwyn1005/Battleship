

import pygame

class GameDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 25)
    
    # Draws player names in the corners
    def draw_names(self, player1, player2):
        player_text = self.font.render(f"Player: {player1}", True, (255, 255, 255))
        opponent_text = self.font.render(f"Opponent: {player2}", True, (255, 255, 255))
        self.screen.blit(player_text, (10, 10))  # top left corner
        self.screen.blit(opponent_text, (self.screen.get_width() - opponent_text.get_width() - 10, 10))  # top right corner
    
    # Draw the turn indicator in the center
    def draw_turn_indicator(self, current_player):
        turn_text = self.font.render(f"Turn: {current_player}", True, (255, 255, 255))
        text_rect = turn_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 6))
        self.screen.blit(turn_text, text_rect)
