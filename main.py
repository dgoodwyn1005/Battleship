#Battleship game using pygame!
#Contains the main game loop

import pygame 

background_colour = (0, 0, 0) 
  
#Game Dimensions
screen = pygame.display.set_mode((1024, 768)) 
pygame.display.set_caption("Battleship") 
screen.fill(background_colour) 
  
pygame.display.flip() 
  
running = True
  
# Main Game Loop
while running: 
     
    for event in pygame.event.get(): 
        
        #Keyboard Input
        if event.type == pygame.QUIT: 
            running = False