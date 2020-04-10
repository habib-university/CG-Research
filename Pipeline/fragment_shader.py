from fragment_processing import *

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

class Program:
    def __init__(self, screen, buffer):
        self.screen = screen
        self.buffer = buffer
        self.frag_processing = None
        self.vertex_shader = None
        self.fragment_shader = None

    def attach_shader(self, shader):
        if isinstance(shader, Fragment_Shader):
            self.fragment_shader = shader
##        elif isinstance(shader, Vertex_Shader):
##            self.vertex_shader = shader

    def enable_test(self, mode):
        if self.fragment_shader != None:
            self.frag_processing = Fragment_Processing(self.fragment_shader.get_fragments(),
                                                       self.buffer)
            if mode == 'alpha':
                self.frag_processing.alpha_test = True
            elif mode == 'blend':
                self.frag_processing.blending = True
            elif mode == 'depth':
                self.frag_processing.depth_test = True
                
        else:
            return 'Valid fragment shader not found'

    #should only be called within draw primitive functions
    def update_fragments(self, frags):
        if self.fragment_shader != None:
            self.fragment_shader.fragments = frags
            #print('fragment shader ', self.fragment_shader.fragments[3580].color)
            if self.frag_processing != None:
                #self.frag_processing.fragments = self.fragment_shader.get_fragments()
                self.frag_processing.set_fragments(self.convert_frags(frags))
                #print('fragment processing ', self.frag_processing.fragments[3580].color)
            
            #print(frags[1300].color)
        if self.frag_processing == None:
            #print('hello')
            self.buffer.set_pixels(frags)

    def send_fragments(self):
        #get fragments after fragment processing
        self.buffer.set_pixels(self.frag_processing.get_fragments())

    def convert_frags(self, frags):
        temp = frags
        for i in range(len(temp)):
            temp[i] = frags[i]
            temp[i].color = self.convert_01(frags[i].color)
        return temp

    def convert_01(self,val):
        temp = []
        for i in range(len(val)):
            temp.append(round(val[i]/255, 5))
        return temp
