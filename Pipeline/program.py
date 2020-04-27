from fragment_processing import *
from fragment_shader import *

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
            if self.frag_processing == None:
                self.frag_processing = Fragment_Processing(self.fragment_shader.get_fragments(),
                                                       self.buffer)
            self.frag_processing.set_test(mode)
##            if mode == 'alpha':
##                self.frag_processing.alpha_test = True
##            elif mode == 'blend':
##                self.frag_processing.blending = True
##            elif mode == 'depth':
##                print(self.frag_processing.alpha_test)
##                self.frag_processing.depth_test = True
##                
        else:
            return 'Valid fragment shader not found'

    #should only be called within draw primitive functions
    def update_fragments(self, frags):
        if self.fragment_shader != None:
            print('jello')
            self.fragment_shader.fragments = frags
            
            if self.frag_processing != None:
                print('hello')
##                if self.frag_processing.blending:
##                    self.frag_processing.set_fragments(self.convert_frags(frags))
##                else:
                self.frag_processing.set_fragments(frags)
        if self.frag_processing == None:
            self.buffer.set_pixels(frags)

    def send_fragments(self):
        #get fragments after fragment processing
        self.buffer.set_pixels(self.frag_processing.get_fragments())

    def convert_frags(self, frags):
        temp = frags
        for i in range(len(temp)):
            temp[i] = frags[i]
            temp[i].color = convert_01(frags[i].color)
        return temp


