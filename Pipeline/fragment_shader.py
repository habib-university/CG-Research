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
        self.frag_color = black
        self.uniforms = None
        self.current_fragment = None
        #frag coord and point coord - built in special variables for fragment shader (not needed for now)

    def get_fragments(self):
        return self.fragments

    def run_shader(self, frags, f, *args):
        for a in range(len(self.fragments)):
            #self.current_fragment = self.fragments[a]
            final_color = f(self.fragments[a].color, frags[a].color)
            self.fragments[a].color = final_color #since we are not receiving any color rn
        return self.fragments
        
