import random
from fragment_processing import *
from fragment_shader import *
from helpers import *

class Program:
    def __init__(self, screen, buffer):
        self.screen = screen
        self.buffer = buffer
        self.frag_processing = None
        self.vertex_shader = None
        self.fragment_shader = None
        self.blend_src = None
        self.blend_dst = None
        self.alpha_const = None
        self.alpha_ref = None
        self.depth_test = False

    def attach_shader(self, shader):
        if isinstance(shader, Fragment_Shader):
            self.fragment_shader = shader
##        elif isinstance(shader, Vertex_Shader):
##            self.vertex_shader = shader

    def enable_test(self, mode):
        if self.frag_processing == None:
            self.frag_processing = Fragment_Processing(None,
                                                       self.buffer)
        self.frag_processing.set_test(mode, True)
        
    def disable_test(self, mode):
        self.frag_processing.set_test(mode, False)

    #runs fragment processing stage
    def run_fragProcessing(self, frags):
        if self.frag_processing != None:
            self.frag_processing.set_fragments(frags)
            if self.frag_processing.alpha_test:
                fragments = self.frag_processing.alpha_func(self.alpha_const, self.alpha_ref)
                self.frag_processing.set_fragments(fragments)
            if self.frag_processing.depth_test and self.depth_test:
                fragments = self.frag_processing.depth_func()
                self.frag_processing.set_fragments(fragments)
            if self.frag_processing.blending:
                self.frag_processing.blend_func(self.blend_src, self.blend_dst)
        else:
            self.buffer.set_pixels(frags)      

    def blend_func(self, src, dst):
        self.blend_src = src
        self.blend_dst = dst

    def alpha_func(self, const, ref):
        self.alpha_const = const
        self.alpha_ref = ref

    def depth_func(self):
        self.depth_test = True
