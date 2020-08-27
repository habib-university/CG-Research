import random
from fragment_processing import *
from fragment_shader import *
from rasterizer import *
from helpers import *
from main import write_fragmentShader

class Program:
    def __init__(self, screen, buffer, blank_frags):
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
        self.blank_frags = blank_frags
        self.rasterizer = Rasterizer(blank_frags)
        self.fragments = None

    def attach_shader(self, shader):
        if isinstance(shader, Fragment_Shader):
            self.fragment_shader = shader
            #self.rasterizer.set_color = self.fragment_shader.get_fragColor()
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

    def send_vertices_data(self, vertices):
        self.rasterizer.set_vertices(vertices)
    
    def send_color_data(self, colors = None):
        self.rasterizer.set_colors(colors)

    def draw_arrays(self, mode, first, count):
        #mode = primitive type, first = starting index, count = no. of vertices to be rendered
        if mode == "POINT":
            self.rasterizer.draw_point(first, count)

    def run_fragment_shader(self):
        frags = self.rasterizer.get_fragments()
        self.fragment_shader.set_blankFrags(self.blank_frags)
        self.fragment_shader.run_shader(frags, write_fragmentShader)
        self.fragments = self.fragment_shader.get_fragments()
    
    def get_fragments(self):
        return self.fragments
