"""
    There maybe multiple fragments generated for a pixel if there is
    multisampling or the use of textures. For our purposes here, we are
    assuming there are no samplers or textures, so one fragment represents
    one pixel.
"""

from framebuffer import Framebuffer
from constants import *

class Scissor_Box:
    def __init__(self, left, bottom, width, height):
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height    

class Fragment:
    def __init__(self, pos, color):
        #position on screen
        self.x = pos[0] 
        self.y = pos[1]
        """
            The interpolated attributes in the fragment includes color and
            texture. Right now we're only considering color.
        """
        self.color = color
        self.depth = False

class Fragment_Processing:
    def __init__(self, fragments, frame_buffer):
        self.fragments = fragments #an array of fragments
        self.frame_buffer = frame_buffer
        self.scissorBox = Scissor_Box(0, 0, WIDTH, HEIGHT)

    def enable_test(self, mode):
        if  mode == 'scissor':
            scissor_test()
        #elif mode == 'depth':
        #    depth_test()

##    def pixel_ownership_test(self):
        
    def scissor_test(self):
        l = self.scissorBox.left
        b = self.scissorBox.bottom
        if self.scissorBox.width < 0 or self.scissorBox.height < 0:
            return 'Error: Invalid value'
        for i in range(len(fragments)):
            if l <= fragments[i].x and (fragments[i].x < l + self.scissorBox.width):
                if b <= fragments[i].y and (fragments[i].y < b + self.scissorBox.height):
                    continue
            return False
        
##    def depth_test(self):
##    

#Functions outside classes in main
def scissor_box(left, bottom, width, height):
    fragment_processing.scissorBox = Scissor_Box(left, bottom, width, height)
      
    
        
        
