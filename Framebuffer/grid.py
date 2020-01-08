import sys
import pygame
import random
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
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
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
running = True
refresh = False
double_buffering = False
frame_buffer = np.zeros((255, 255, 3))

#update after interval
DISPLAY = pygame.USEREVENT + 1
pygame.time.set_timer(DISPLAY, 16)

while running:
      
    # process inputs(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == DISPLAY and not refresh:
            refresh = True
            #get buffer info
            #s = pygame.surfarray.pixels3d(screen)

            #update buffer info
            for i in range(len(frame_buffer)):
                for j in range(len(frame_buffer[i])):
                    if np.all(frame_buffer[i][j]):
                        frame_buffer[i][j] = [255,0,0]
            pygame.surfarray.blit_array(screen, frame_buffer)
            
        elif event.type == DISPLAY and refresh:
            refresh = False
            
    #draw grid
    if not refresh:
        screen.fill(black)
        for y in range(margin, HEIGHT, width+margin):
            for x in range(margin, HEIGHT, width+margin):
                for i in range(width+1):
                    frame_buffer[y][x+i] = [255, 255, 255]
                    frame_buffer[y+i][x] = [255, 255, 255]
                    frame_buffer[y+width][x+i] = [255, 255, 255]    
                    frame_buffer[y+i][x+width] = [255, 255, 255]
        pygame.surfarray.blit_array(screen, frame_buffer)

    pygame.display.update()
    
pygame.quit()
