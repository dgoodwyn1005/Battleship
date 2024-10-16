# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 20:18:45 2024

@author: alepine
"""

import pygame

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font, color: tuple, text_color: tuple):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)  
        self.text = text  
        self.font = font  
        self.color = color  
        self.text_color = text_color  

    def draw(self, screen: pygame.Surface):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        
        # Center text inside the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Draw the text
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        
        #Check if the button is pressed, true if it is, false if it isnt
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 20:18:45 2024

@author: alepine
"""

import pygame

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font, color: tuple, text_color: tuple):
        self.rect = pygame.Rect(x, y, width, height)  
        self.text = text  
        self.font = font  
        self.color = color  
        self.text_color = text_color

    def draw(self, screen: pygame.Surface):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        
        # Center text inside the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Draw the text
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        
        #Check if the button is pressed
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
