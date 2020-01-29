"""
    There maybe multiple fragments generated for a pixel if there is
    multisampling or the use of textures. For our purposes here, we are
    assuming there are no samplers or textures, so one fragment represents
    one pixel.
"""

from framebuffer import Framebuffer
from constants import *

class Scissor_Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box = True
        

class Fragment:
    def __init__(self, pos, color):
        self.pos = pos #position on screen

        """
            The interpolated attributes in the fragment includes color and
            texture. Right now we're only considering color.
        """
        self.color = color

class Fragment_Processing:
    def __init__(self, fragment, frame_buffer, scissor_box):
        self.fragment = fragment
        self.frame_buffer = frame_buffer
        self.scissorBox = scissor_box

    def enable_test(self, mode):
        if  mode == 'scissor':
            scissor_test()
        #elif mode == 'stencil':
        #    stencil_test()
        #elif mode == 'depth':
        #    depth_test()

##    def pixel_ownership_test(self):
        
    def scissor_test(self):
        if left <= x and (x < left + width):
            if bottom <= y and (y < bottom + height):
                return True
        return False
        
##    def stencil_test(self):
##    def depth_test(self):
##    

def scissor_box(x, y, width, height):
    if not scissorBox:
        width = WIDTH
        height = HEIGHT
    else:
        scissorBox = True
    #Add code if x, y, width, height are actually specified
    
        
        
