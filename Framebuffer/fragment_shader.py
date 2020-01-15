import pygame
from framebuffer import Framebuffer
from constants import *

"""
    This file contains the code for fragment shader.
"""
        
#width and height of grid
WIDTH = 255
HEIGHT = 255

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Grid")

#initialize variables
width = height = 20
margin = 5
running = True
refresh = False
frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)

#update after interval
DISPLAY = pygame.USEREVENT + 1
pygame.time.set_timer(DISPLAY, 16)

##SWITCH = pygame.USEREVENT + 2
##pygame.time.set_timer(SWITCH, 16)


while running:

    frame_buffer.draw(white)
    
    # process inputs(events)
    for event in pygame.event.get():
        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                frame_buffer.enable_doubleBuffering()

        elif event.type == DISPLAY and not refresh:
            refresh = True

        elif event.type == DISPLAY and refresh:
            refresh = False
    
    frame_buffer.set_buffer(refresh)
    pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())

    pygame.display.update()
    
pygame.quit()
