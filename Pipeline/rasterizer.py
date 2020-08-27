from primitive import *
from helpers import *

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

    def draw_point(self, first, count):
        vertices = self.vertices[first:]
        vertices = self.vertices[:count]
        
        block_size = 20
        margin = 5
        #computing colors array if color is directly given in fragment shader
        if self.colors == None:
            color = self.colors
            self.colors = []
            for i in range(len(vertices)):
                self.colors.append([0,0,0,1])
        colors = self.colors[first:]
        colors = self.colors[:count]
        
        #light up pixels for where the vertices given
        for i in range(len(vertices)):
            new_coord = coordinate_conversion(vertices[i][0], vertices[i][1], block_size, margin)
            point = Point((new_coord[0], new_coord[1], vertices[i][2]), colors[i])
            self.fragments = point.draw(new_coord[0], new_coord[1], vertices[i][2], colors[i], self.fragments)

    def get_fragments(self):
        return self.fragments
