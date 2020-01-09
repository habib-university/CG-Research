import pygame
import random
import numpy as np

#class for frame buffers
class Framebuffer:
    def __init__(self, width, height, margin, grid_width, grid_height):
        self.width = width 
        self.height = height
        self.margin = margin
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.buffer = np.zeros((grid_width, grid_height, 3))

    def clear(self):
        for y in range(self.margin, HEIGHT, self.width + self.margin):
                for x in range(self.margin, WIDTH, self.width + self.margin):
                    for i in range(self.width + 1):
                        buffer[y][x+i] = [255, 255, 255]
                        buffer[y+i][x] = [255, 255, 255]
                        buffer[y+width][x+i] = [255, 255, 255]    
                        buffer[y+i][x+width] = [255, 255, 255]

    def draw(self, color):
        for y in range(margin, HEIGHT, width+margin):
            for x in range(margin, WIDTH, width+margin):
                for i in range(width+1):
                    self.buffer[y][x+i] = color
                    self.buffer[y+i][x] = color
                    self.buffer[y+self.height][x+i] = color  
                    self.buffer[y+i][x+self.width] = color

    def get_buffer(self):
        return self.buffer
        
#width and height of grid
WIDTH = 255
HEIGHT = 255

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Grid")

#colors
black = [0,0,0]
white = [255, 255, 255]
red = [255, 0, 0]

#initialize variables
width = height = 20
margin = 5
running = True
refresh = False
double_buffering = False
frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)
front_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)
back_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)


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
            if event.key == pygame.K_d and not double_buffering:
                double_buffering = True
            
        elif event.type == DISPLAY and not refresh and not double_buffering:
            refresh = True
            frame_buffer.draw(white)
            pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())

        elif event.type == DISPLAY and refresh:
            refresh = False
            
    #draw grid
    if not double_buffering and not refresh:
        frame_buffer.draw(white)
        pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())

    if double_buffering:
        back_buffer.draw(red)
        if not refresh:
            back_buffer, front_buffer = front_buffer, back_buffer
            pygame.surfarray.blit_array(screen, front_buffer.get_buffer())
        
    pygame.display.update()
    
pygame.quit()
