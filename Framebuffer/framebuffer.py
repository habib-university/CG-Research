import numpy as np
from constants import *

"""
    This file represents a class for frame buffer object.
"""

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
        for y in range(self.margin, self.grid_height, self.width + self.margin):
            for x in range(self.margin, self.grid_width, self.width + self.margin):
                for n in range(self.width+1):
                    for j in range(self.width+1):
                        temp = y+n
                        if self.double_buffer:
                            self.back_buffer[temp][x+j] = color
                        else:
                            self.front_buffer[temp][x+j] = color
    
    def draw_face(self, color):
        for y in range(self.margin, self.grid_height, self.width + self.margin):
            for x in range(self.margin, self.grid_width, self.width + self.margin):
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

    def set_buffer(self, refresh):
        if not self.double_buffer and refresh:
            np.copyto(self.front_buffer, self.front_buffer)
        elif self.double_buffer and refresh:
            np.copyto(self.front_buffer, self.back_buffer)
        elif self.double_buffer and not refresh:
            np.copyto(self.front_buffer, self.back_buffer)
            self.front_buffer, self.back_buffer = self.back_buffer, self.front_buffer
        
    def get_buffer(self):
        return self.front_buffer
    
