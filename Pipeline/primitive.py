from helpers import *
from fragment_shader import *

class Point:
    def __init__(self, vertices, color):
        self.x = vertices[0]
        self.y = vertices[1]
        #By default it is 1, and needs to be enabled
        self.pointSize= 1
    
    def draw(self, x, y, z, color, fragments):
        block_size = 20
        x_Limit = x + block_size
        y_Limit = y + block_size
        for i in range(len(fragments)):
            x_pos = fragments[i].buffer_pos[0]
            y_pos = fragments[i].buffer_pos[1]
            
            if (x_pos >= x and x_pos <= x_Limit) and (y_pos >= y and y_pos <= y_Limit):
                fragments[i].is_color = True
                if fragments[i].color == [255, 255, 255, 255] or fragments[i].color == [1,1,1,1]:
                    fragments[i].color = color
                    fragments[i].depth = z
                else:
                    pos = [fragments[i].buffer_pos[0], fragments[i].buffer_pos[1], z]
                    fragments.append(Fragment(color, pos))
                    fragments[-1].is_color = True
            else:
                color_bool = check_255(fragments[i].color)
                if color_bool:
                    new_color = convert_01(fragments[i].color)
                    fragments[i].color = new_color
        return fragments