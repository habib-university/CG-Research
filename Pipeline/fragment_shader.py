from fragment_processing import *
from helpers import *

class Fragment:
    def __init__(self, color, buffer_pos):
        #position on screen in NDC (between 1 and -1)
        #self.x = pos[0] 
        #self.y = pos[1]
        #self.z = pos[2]
        self.buffer_pos = buffer_pos
        """
            Position will be a vec3 = (x,y,z) and color will be vec4 = (R,G,B,A)
            The interpolated attributes in the fragment includes color and
            texture. Right now we're only considering color.
        """
        self.color = color  #vec4
        self.depth = buffer_pos[2]

##class Pixel:
##    def __init__(self, pos, color, depth):
##        self.buffer_position = pos
##        self.color = color
##        self.depth = depth

class Fragment_Shader:
    def __init__(self, fragments):
        self.fragments = fragments

    def set_fragColor(self, color):
        self.frag_color = color

    def get_fragments(self):
        return self.fragments

    def run_shader(self):
        ####only apply color to primitives
        
        #for a in range(len(self.fragments)):
        #    self.fragments[a].color = self.frag_color
        return self.fragments
