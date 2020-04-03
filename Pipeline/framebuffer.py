"""
    This file represents a class for frame buffer object.
"""
import sys
import asyncio
import numpy as np
import time
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
        #two color buffers, front and back
        self.front_buffer = np.zeros((grid_width, grid_height, 3))
        self.back_buffer = np.zeros((grid_width, grid_height, 3))
        self.depth_buffer = np.ones((grid_width,grid_height,1))
        self.visible = False

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
###########TEST FUNCTIONS
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
                    if self.double_buffer and not self.visible:
                        self.back_buffer[y][x:x+self.width] = color
                    else:
                        self.front_buffer[y][x:x+self.width] = color
            
    def draw_lines(self, color):
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
                    if self.double_buffer and not self.visible:
                        self.back_buffer[y][x:x+self.width] = color
                        if (x >= 55 and x <= 75) or (y >= 55 and y <= 75):
                            self.back_buffer[y][x:x+self.width] = green
                    else:
                        self.front_buffer[y][x:x+self.width] = color
                        if (x >= 55 and x <= 75) or (y >= 55 and y <= 75):
                            self.front_buffer[y][x:x+self.width] = green
        
    def draw_plus(self, color):
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
                    if self.double_buffer and not self.visible:
                        self.back_buffer[y][x:x+self.width] = color
                        if (x >= 80 and x <= 150) or (y >= 80 and y <= 150):
                            self.back_buffer[y][x:x+self.width] = green
                    else:
                        self.front_buffer[y][x:x+self.width] = color
                        if (x >= 80 and x <= 150) or (y >= 80 and y <= 150):
                            self.front_buffer[y][x:x+self.width] = green          

    def draw_loops(self, color):
        for y in range(self.margin, self.grid_height, self.width + self.margin):
            for x in range(self.margin, self.grid_width, self.width + self.margin):
                for n in range(self.width):
                    for j in range(self.width):
                        temp = y+n
                        if self.double_buffer and not self.visible:
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

    def buffer_status(self):
        return self.double_buffer

    def set_buffer(self, refresh):
        if self.double_buffer and not refresh:
            if not self.visible:
                #np.copyto(self.front_buffer, self.back_buffer)
                self.front_buffer, self.back_buffer = self.back_buffer, self.front_buffer
                self.visible = True
            elif self.visible:
                #np.copyto(self.back_buffer, self.front_buffer)
                self.front_buffer, self.back_buffer = self.back_buffer, self.front_buffer
                self.visible = False
                
    def get_buffer(self):
        return self.front_buffer
    
    def set_pixels(self, fragments):
        for i in range(len(fragments)):
            pos = fragments[i].buffer_pos
            self.front_buffer[pos[0]][pos[1]] = fragments[i].color[:3]
        
    def set_depth(self,pos,depth,color):
        self.depth_buffer[pos[1]][pos[0]] = depth
        self.front_buffer[pos[1]][pos[0]] = color
        
    def getdepthBuffer(self):
        return self.depth_buffer
    
    def clear_depthBuffer(self):
        self.depth_buffer = np.ones((grid_width,grid_height,1))
