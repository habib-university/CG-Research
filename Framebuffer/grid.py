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
frame_buffer = np.zeros((255, 255, 3))

#update after interval
DISPLAY = pygame.USEREVENT + 1
pygame.time.set_timer(DISPLAY, 5000)
#pygame.time.set_timer(DISPLAY, 16)

while running:
      
    # process inputs(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == DISPLAY and not refresh:
            print('Refresh screen')
            refresh = True
                
            #get buffer info
            s = pygame.surfarray.pixels3d(screen)
            frame_buffer = s
            #print(s)
            #update buffer info
            #for i in range(len(frame_buffer)):
            #    for j in range(len(frame_buffer[i])):
            #        if np.all(frame_buffer[i][j]):
            #            frame_buffer[i][j] = [255,0,0]
            #frame_buffer[random.randrange(len(frame_buffer))] = [255,0,0]
            pygame.surfarray.blit_array(screen, frame_buffer)
            print('done')
            
        elif event.type == DISPLAY and refresh:
            refresh = False
            
    #draw grid
    if not refresh:
        screen.fill(black)
        for y in range(margin, HEIGHT, width+margin):
            for x in range(margin, HEIGHT, width+margin):
                rect = pygame.Rect(y, x, width, height)
                pygame.draw.rect(screen, white, rect)

    pygame.display.update()
    
pygame.quit()
