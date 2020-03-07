class Fragment:
    def __init__(self, pos, color):
        #position on screen
        self.x = pos[0] 
        self.y = pos[1]
        """
            The interpolated attributes in the fragment includes color and
            texture. Right now we're only considering color.
        """
        self.color = color  #vec4
        self.depth = False

class Pixel:
    def __init__(self, pos, color, depth):
        self.buffer_position = pos
        self.color = color
        self.depth = depth

class Fragment_Shader:
    def __init__(self, fragments, color):
        self.frag_color = color
        self.fragments = fragments

    def run_shader(self):
        for i in range(len(self.fragments)):
            self.fragments[i].color = self.frag_color
        return self.fragments
        
