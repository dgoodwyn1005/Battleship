import pygame
import pygame.image
import Constants as C
import Display as D
import GameGrid
import Button as B


class BattleScreen(D.Display):

    def __init__(self):
        super().__init__()
        self.running = True
        self.pause_button = B.Button(C.PAUSE_X, C.PAUSE_Y, C.PAUSE_WIDTH_HEIGHT, C.PAUSE_WIDTH_HEIGHT,
                                     C.PAUSE_TEXT, C.font, C.BLACK_BACKGROUND_COLOR, C.WHITE_FONT_COLOR)

        # Load Game Assets
        grid_tile = pygame.image.load(C.IMAGE_FOLDER + "/grid.png")
        self.grid_tile = pygame.transform.scale(grid_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))
        self.grid_tile.set_alpha(C.TILE_TRANSPARENCY)
        self.water_tile = pygame.image.load(C.IMAGE_FOLDER + "/water_tile.jpg")
        self.water_tile = pygame.transform.scale(self.water_tile, (C.TILE_WIDTH, C.TILE_HEIGHT))

    # Main Game Loop

    def main_loop(self):

        while self.running:

            for event in pygame.event.get():

                # Keyboard Input
                if event.type == pygame.QUIT:
                    self.running = False
                # Check if it is clicked
                if self.pause_button.is_clicked():
                    print("Clicked")

    def create_grid(self):

        # Player and opponent names, and turn message
        player_name = "Player1"
        opponent_name = "Player2"
        turn_message = "Turn: Player1"

        # Initialize Game Grid
        grid = GameGrid.gamegrid(C.NUM_ROWS, C.NUM_COL)

        for x in range(grid.grid_length()):
            for y in range(grid.grid_height()):
                D.Display.blit(self, self.water_tile, (x * C.TILE_WIDTH, y * C.TILE_HEIGHT))
                D.Display.blit(self, self.grid_tile, (x * C.TILE_WIDTH, y * C.TILE_HEIGHT))

        # Draw the player turn message
        turn_text = C.font.render(turn_message, True, C.WHITE_FONT_COLOR)
        D.Display.blit(self, turn_text, (D.Display.get_width(self) // 2 - turn_text.get_width() // 2, 20))

        # Draw the player name in the left corner
        player_text = C.font.render(f"Player: {player_name}", True, C.WHITE_FONT_COLOR)
        D.Display.blit(self, player_text, (0, 0))

        # Draw the opponent name in the right corner
        opponent_text = C.font.render(f"Opponent: {opponent_name}", True, C.WHITE_FONT_COLOR)
        D.Display.blit(self, opponent_text, (D.Display.get_width(self) - opponent_text.get_width(), 0))

        # Draw pause button
        self.pause_button.draw(self.screen)

        pygame.display.flip()


battle = BattleScreen()
battle.create_grid()
battle.main_loop()
