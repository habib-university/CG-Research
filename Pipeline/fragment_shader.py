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
        self.is_color = False

class Fragment_Shader:
    def __init__(self, fragments=None):
        self.fragments = fragments
        self.frag_color = black
        self.uniforms = None
        self.current_fragment = None
        self.colors = None
        #frag coord and point coord - built in special variables for fragment shader (not needed for now)

    def get_fragments(self):
        return self.fragments

    def get_fragColor(self):
        return self.frag_color
    
    def set_blankFrags(self, blank_frags):
        self.fragments = blank_frags


    def run_shader(self, frags, f, *args):
        final_color = self.frag_color
        for a in range(len(self.fragments)):
            if frags[a].is_color:
                final_color = f(self.fragments[a].color, frags[a].color)
                self.fragments[a].color = final_color #Apply the final color given in fragment shader
        #self.frag_color = final_color #if constant color is given in programmable fragment shader