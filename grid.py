import pygame
import random
import numpy as np

#width and height of grid
WIDTH = 255
HEIGHT = 255

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Grid")

#initialize variables
block_size = 20
width = height = 20
margin = 5
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
running = True
refresh = False


while running:
    
                
    # process inputs(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #pressing R key refreshes screen
            if event.key == pygame.K_r:
                print('Refresh screen')
                refresh = True
                
                #get buffer info
                s = pygame.surfarray.pixels3d(screen)
                
                #update buffer info
                for i in range(len(s)):
                    for j in range(len(s[i])):
                        if np.all(s[i][j]):
                            s[i][j] = [255,0,0]
                out = pygame.surfarray.make_surface(s)
                del s
                screen.blit(out, (0,0))
                print('done')
                
    #draw grid
    if refresh == False:
        screen.fill(black)
        for y in range(margin, HEIGHT, width+margin):
            for x in range(margin, HEIGHT, width+margin):
                rect = pygame.Rect(y, x, block_size, block_size)
                pygame.draw.rect(screen, white, rect)
    
    pygame.display.update()
    
pygame.quit()
