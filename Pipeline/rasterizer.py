from primitive import *
from helpers import *
from constants import *
from bressenham import *

class Vertex:
    def __init__(self, points, attributes = None):
        self.points = points
        self.attributes = attributes

class Rasterizer:
    def __init__(self, blank_frags, vertices = None, colors = None):
        self.vertices = vertices
        self.colors = colors
        self.fragments = blank_frags
        self.primitive_array = []

    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_colors(self, colors):
        self.colors = colors

    def get_fragments(self):
        return self.fragments

    def draw_point(self, first, count):
        vertices = self.vertices[first:count]
        #computing colors array if color is directly given in fragment shader
        if self.colors == None:
            self.colors = []
            for i in range(len(vertices)):
                self.colors.append([0,0,0,1])
        colors = self.colors[first:count]
        
        #light up pixels for where the vertices given
        for i in range(len(vertices)):
            new_coord = coordinate_conversion(vertices[i][0], vertices[i][1], block_size, margin)
            point = Point((new_coord[0], new_coord[1], vertices[i][2]), colors[i])
            self.fragments = point.draw(self.fragments)

    def draw_line(self, first, count):
        vertices = self.vertices[first:count]

        #if self.colors == None:
        #    self.colors = []
        #    for i in range(len(vertices)):
        #        self.colors.append([0,0,0,1])
        #print('colors ', self.colors)
        
        for i in range(0, (len(vertices)//2) + 1, 2):
            line = Line((vertices[i], vertices[i+1]), self.colors[i])
            self.fragments = line.draw(self.fragments)