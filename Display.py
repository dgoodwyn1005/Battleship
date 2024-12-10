import pygame
import Constants as C
class Display(object):

    def __init__(self, width=C.DISPLAY_WIDTH, height=C.DISPLAY_HEIGHT,
                 screenName=C.DEFAULT_CAPTION, background=C.LIGHTER_BLUE_COLOR):
        self.width = width
        self.height = height
        self.screenName = screenName
        self.background = background    # Background Color
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(screenName)
        self.screen.fill(background)
        self.running = True  # Flag to keep the display running

    def startDisplay(self, gameLoop):
        """Start the display and runs the game loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            gameLoop()
            pygame.display.flip()

    def blit(self, image, position):
        """Draws the image on the screen at the given position"""
        self.screen.blit(image, position)

    def get_width(self):
        """Returns the width of the display"""
        return self.screen.get_width()
