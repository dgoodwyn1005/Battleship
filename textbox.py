import pygame
import Constants as C

class TextBox(object):
    def __init__(self, x, y, width, height, font, is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = C.GREY
        self.color_active = C.WHITE_FONT_COLOR
        self.color = self.color_inactive
        self.font = font
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.is_password = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_inactive
            

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                username = self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)
            # Update the text surface based on whether this is a password field
            if self.is_password:
                display_text = '*' * len(self.text)  # Show asterisks for password
            else:
                display_text = self.text  # Show the actual text
            self.txt_surface = self.font.render(display_text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
