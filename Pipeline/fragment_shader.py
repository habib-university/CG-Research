"""
    This file contains code for fragment shader stage of the pipeline.
    It sets colors according to the value specified in the programmable fragment shader.
"""

class Fragment_Shader:
    def __init__(self, fragments=None):
        self.fragments = fragments
        self.frag_color = [0,0,0,1] #if nothing is specified, render black
        self.uniforms = None
        #point coord - built in special variable for fragment shader (not needed for now)

    def get_fragments(self):
        return self.fragments

    def get_fragColor(self):
        return self.frag_color
    
    def set_blankFrags(self, blank_frags): #set fragments array for output
        self.fragments = blank_frags

    def run_shader(self, frags, f, *args):
        final_color = self.frag_color
        for a in range(len(self.fragments)):
            if frags[a].is_color:
                final_color = f(self.fragments[a].color, frags[a].color)
                self.fragments[a].color = final_color #Apply the final color passed through fragment shader