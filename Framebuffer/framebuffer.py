"""
    This file represents a class for frame buffer object.
"""
import sys
import numpy as np
from constants import *
np.set_printoptions(threshold=sys.maxsize)

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
        y_write = False
        n = self.margin
        for y in range(self.margin, self.grid_height-self.margin):
            if y == n:
                if not y_write:
                    n += self.width
                    y_write = True
                elif y_write:
                    n += self.margin
                    y_write = False
            m = self.margin
            for x in range(self.margin, self.grid_width-self.margin):
                if y_write and x == m:
                    self.front_buffer[y][x:x+self.width] = white
                    m += self.width + self.margin

    def draw(self, color):
        y_write = False
        n = self.margin
        for y in range(self.margin, self.grid_height-self.margin):
            if y == n:
                if not y_write:
                    n += self.width
                    y_write = True
                elif y_write:
                    n += self.margin
                    y_write = False
            m = self.margin
            for x in range(self.margin, self.grid_width-self.margin):
                if y_write and x == m:
                    m += self.width + self.margin
                    if self.double_buffer:
                        self.back_buffer[y][x:x+self.width] = color
                    else:
                        self.front_buffer[y][x:x+self.width] = color
            
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
        print('double buffering enabled')
        self.double_buffer = True

    def set_buffer(self, refresh):
     
        if refresh:
            np.copyto(self.front_buffer, self.front_buffer)

        if self.double_buffer and not refresh:
            #np.copyto(self.front_buffer, self.back_buffer)
            self.front_buffer, self.back_buffer = self.back_buffer, self.front_buffer

    def get_buffer(self):
        return self.front_buffer
    
