"""
    This file contains primitive classes (point and line).
    Primitive is tha parent class whose child classes are Point and Line.
    These classes implement the algorithms required to find which fragments would be rendered,
    apply color and return the fragments with that information.
"""

import helpers
from constants import block_size, margin
from fragment import Fragment
from abc import ABCMeta, abstractmethod

#Parent primitive class
class Primitive(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, fragments):
        pass

class Point(Primitive):
    def __init__(self, vertex, color):
        self.x = vertex[0]
        self.y = vertex[1]
        self.z = vertex[2]
        self.color = color
        #By default it is 1, and needs to be enabled
        self.pointSize= 1
    
    def draw(self, fragments):
        x_Limit = self.x + block_size
        y_Limit = self.y + block_size
        for i in range(len(fragments)):
            x_pos = fragments[i].buffer_pos[0]
            y_pos = fragments[i].buffer_pos[1]
            
            #Check if fragment is the point, then apply color and depth
            if (x_pos >= self.x and x_pos <= x_Limit) and (y_pos >= self.y and y_pos <= y_Limit):
                fragments[i].is_color = True
                if fragments[i].color == [255, 255, 255, 255] or fragments[i].color == [1,1,1,1]:
                    fragments[i].color = self.color
                    fragments[i].depth = self.z
                else:
                    pos = [fragments[i].buffer_pos[0], fragments[i].buffer_pos[1], self.z]
                    fragments.append(Fragment(self.color, pos))
                    fragments[-1].is_color = True
            else:
                color_bool = helpers.check_255(fragments[i].color)
                if color_bool:
                    new_color = helpers.convert_01(fragments[i].color)
                    fragments[i].color = new_color
        return fragments

class Line(Primitive):
    def __init__(self, vertices, color):
        self.start = vertices[0]
        self.end = vertices[1]
        self.color = color
    
    def draw(self, fragments):
        #Get points from Bresenham Algorithm
        points = self.bresenham()
        #Draw points
        for i in range(len(points)):
            new_coord = helpers.coordinate_conversion(points[i][0], points[i][1], block_size, margin)
            point = Point((new_coord[0], new_coord[1], points[i][2]), self.color)
            frags = point.draw(fragments)
        return frags
    
    def bresenham(self): #Bresenham's algorithm for line rasterization
        x0, y0, z0, x1, y1, z1 = self.start[0], self.start[1], self.start[2], self.end[0], self.end[1], self.end[2]
        if (abs(y1 - y0) < abs(x1 - x0)):
            if x0 > x1:
                return self.negative_line(x1, y1, z1, x0, y0, z0)
            else:
                return self.negative_line(x0, y0, z0, x1, y1, z1)
        else:
            if y0 > y1:
                return self.positive_line(x1, y1, z1, x0, y0, z0)
            else:
                return self.positive_line(x0, y0, z0, x1, y1, z1)

    def positive_line(self, x0, y0, z0, x1, y1, z1):
        values = []
        deltaX = x1 - x0
        deltaY = y1 - y0
        xi = 1
        if deltaX < 0:
            xi = -1
            deltaX = -deltaX
        D = 2 * deltaX - deltaY
        xVal = x0

        for yVal in range(y0, y1):
            values.append([xVal, yVal, z0])
            if D > 0:
                xVal = xVal + xi
                D = D - 2 * deltaY
            D = D + 2 * deltaX
        values.append([x1, y1, z1])
        return values

    def negative_line(self, x0, y0, z0, x1, y1, z1):
        values = []
        deltaX = x1 - x0
        deltaY = y1 - y0
        yi = 1
        if deltaY < 0:
            yi = -1
            deltaY = deltaY * -1
        D = 2*deltaY - deltaX
        yVal = y0

        for xVal in range(x0, x1):
            values.append([xVal, yVal, z0])
            if D > 0:
                yVal = yVal +yi
                D = D - 2*deltaX
            D = D + 2*deltaY
        values.append([x1, y1, z1])
        return values