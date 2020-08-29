"""
    This file implements the rasterization stage of the pipeline.
    It checks which vertices were provided by the user and
    sets the flag of the respective fragment for coloring.
"""

import helpers
from primitive import Point, Line
from constants import block_size, margin

class Rasterizer:
    def __init__(self, blank_frags, vertices = None, colors = None):
        self.vertices = vertices
        self.colors = colors
        self.fragments = blank_frags
        self.primitive_array = []

    def set_vertices(self, vertices): #set vertices given in array
        self.vertices = vertices

    def set_colors(self, colors): #set colors given in array
        self.colors = colors

    def get_fragments(self): #send final fragments from rasterizer
        return self.fragments

    def draw_point(self, first, count):
        vertices = self.vertices[first:count]
        #if no colors are given
        if self.colors == None:
            self.colors = []
            for i in range(len(vertices)):
                self.colors.append([0,0,0,1])
        colors = self.colors[first:count]
        
        #light up pixels for where the vertices given
        for i in range(len(vertices)):
            new_coord = helpers.coordinate_conversion(vertices[i][0], vertices[i][1], block_size, margin)
            point = Point((new_coord[0], new_coord[1], vertices[i][2]), colors[i])
            self.fragments = point.draw(self.fragments)

    def draw_line(self, first, count):
        vertices = self.vertices[first:count]
        #if no colors are given
        if self.colors == None:
            self.colors = []
            for i in range(len(vertices)):
                self.colors.append([0,0,0,1])
        colors = self.colors[first:count]

        #two points in vertices array will represent start and end of line, light up their pixels
        for i in range(0, (len(vertices)//2) + 1, 2):
            line = Line((vertices[i], vertices[i+1]), colors[i])
            self.fragments = line.draw(self.fragments)