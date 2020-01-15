import pygame
import random
import numpy as np


#colors
black = [0,0,0]
white = [255, 255, 255]
red = [255, 0, 0]

#class for frame buffers
class Framebuffer:
    def __init__(self, width, height, margin, grid_width, grid_height):
        self.width = width 
        self.height = height
        self.margin = margin
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.double_buffer = False
        self.front_buffer = np.zeros((grid_width, grid_height, 3))
        self.back_buffer = np.zeros((grid_width, grid_height, 3))

    def clear(self):
        for y in range(self.margin, self.grid_height, self.width + self.margin):
            for x in range(self.margin, self.grid_width, self.width + self.margin):
                for n in range(self.width+1):
                    for j in range(self.width+1):
                        temp = y+n
                        if self.double_buffer:
                            self.back_buffer[temp][x+j] = white
                        else:
                            self.front_buffer[temp][x+j] = white

    def draw(self, color):
        for y in range(self.margin, HEIGHT, self.width + self.margin):
            for x in range(self.margin, WIDTH, self.width + self.margin):
                for n in range(self.width+1):
                    for j in range(self.width+1):
                        temp = y+n
                        if self.double_buffer:
                            self.back_buffer[temp][x+j] = color
                        else:
                            self.front_buffer[temp][x+j] = color
    
    def draw_face(self, color):
        for y in range(self.margin, HEIGHT, self.width + self.margin):
            for x in range(self.margin, WIDTH, self.width + self.margin):
                for n in range(self.width+1):
                    for j in range(self.width+1):
                        temp = y+n
                        if self.double_buffer:
                            self.back_buffer[temp][x+j] = color
                            self.back_buffer[55+n][55+j] = black #eyes
                            self.back_buffer[180+n][55+j] = black
                            self.back_buffer[80+n][155+j] = black #mouth
                            self.back_buffer[105+n][155+j] = black
                            self.back_buffer[130+n][155+j] = black
                            self.back_buffer[155+n][155+j] = black
                        else:
                            self.front_buffer[temp][x+j] = color
                            self.front_buffer[55+n][55+j] = black #eyes
                            self.front_buffer[180+n][55+j] = black
                            self.front_buffer[80+n][155+j] = black #mouth
                            self.front_buffer[105+n][155+j] = black
                            self.front_buffer[130+n][155+j] = black
                            self.front_buffer[155+n][155+j] = black
                            
    def enable_doubleBuffering(self):
        self.double_buffer = True

    def bufferStatus(self):
        return self.double_buffer
    
    def set_buffer(self, refresh):
        if self.double_buffer and not refresh:
            np.copyto(self.front_buffer, self.back_buffer)
            self.front_buffer, self.back_buffer = self.back_buffer, self.front_buffer
        
    def get_buffer(self):
        return self.front_buffer
        
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
double_buffering = False
frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)

#update after interval
DISPLAY = pygame.USEREVENT + 1
pygame.time.set_timer(DISPLAY, 16)

while running:
      
    # process inputs(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_d:
                frame_buffer.enable_doubleBuffering()
                double_buffering = True
            
        elif event.type == DISPLAY and not refresh:
            refresh = True
            frame_buffer.draw(white)
            pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())

        elif event.type == DISPLAY and refresh:
            refresh = False
            
    #draw grid
    #if not double_buffering and not refresh:
    #    frame_buffer.draw(white)
    #    pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())

    if frame_buffer.bufferStatus():
        frame_buffer.draw(red)
    else:
        frame_buffer.draw(white)
    frame_buffer.set_buffer(refresh)

    
    
    #if double_buffering:    
        #back_buffer.draw(red)
        #if not refresh:
            #back_buffer, front_buffer = front_buffer, back_buffer
    pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())
        
    pygame.display.update()
    
pygame.quit()
