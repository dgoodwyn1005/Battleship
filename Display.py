import pygame
import Constants as C
class Display(object):

    def __init__(self, width = C.DISPLAY_WIDTH, height = C.DISPLAY_HEIGHT,
                 screenName = C.DEFAULT_CAPTION, background = C.LIGHTER_BLUE_COLOR):
        self.width = width
        self.height = height
        self.screenName = screenName
        self.background = background
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(screenName)
        self.screen.fill(background)
        self.running = True

    def startDisplay(self, gameLoop):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            gameLoop()
            pygame.display.flip()

    def changeDimensions(self, width, height):
        self.screen = pygame.display.set_mode((width, height))

    def blit(self, image, position):
        self.screen.blit(image, position)

    def get_width(self):
        return self.screen.get_width()

