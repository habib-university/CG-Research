"""
    This file implements the program which links different parts of the pipeline,
    and transfers data from one stage to another.
"""

import random
import helpers
from fragment_processing import Fragment_Processing
from fragment_shader import Fragment_Shader
from rasterizer import Rasterizer
from user_program import write_fragmentShader

class Program:
    def __init__(self, screen, buffer):
        self.screen = screen
        self.buffer = buffer
        self.fragments = None
        self.blank_frags = None
        #pipeline stages
        self.frag_processing = None
        self.vertex_shader = None
        self.fragment_shader = None
        self.rasterizer = None
        #bools for fragment processing stage
        self.blend_src = None
        self.blend_dst = None
        self.alpha_const = None
        self.alpha_ref = None
        self.depth_test = False

    def get_fragments(self): #send fragments to main
        return self.fragments

    def check_errors(self):
        if self.fragment_shader == None:
            raise Exception('You did not specify fragment shader!')
        
    def attach_shader(self, shader):
        self.blank_frags = helpers.buffer_to_fragments(self.buffer.get_buffer(), 0, self.buffer.alpha)
        self.rasterizer = Rasterizer(self.blank_frags)
        if isinstance(shader, Fragment_Shader):
            self.fragment_shader = shader
        else: 
            raise Exception('You did not specify correct shader!')
##        elif isinstance(shader, Vertex_Shader):
##            self.vertex_shader = shader

    """ Rasterizer functions in program """
    def send_vertices_data(self, vertices):
        self.check_errors()
        self.rasterizer.set_vertices(vertices)
    
    def send_color_data(self, colors = None):
        self.rasterizer.set_colors(colors)

    def draw_arrays(self, mode, first, count):
        #mode = primitive type, first = starting index, count = no. of vertices to be rendered
        if self.rasterizer.vertices == None:
            return
        if mode == "POINT":
            self.rasterizer.draw_point(first, count)
        elif mode == "LINE":
            self.rasterizer.draw_line(first, count)
        if not self.frag_processing.blending:
            self.fragments = self.rasterizer.get_fragments()
            self.buffer.set_pixels(self.fragments)  


    """Fragment shader function in program"""
    def run_fragment_shader(self):
        frags = self.rasterizer.get_fragments()
        self.fragment_shader.set_blankFrags(self.blank_frags)
        self.fragment_shader.run_shader(frags, write_fragmentShader)
        self.fragments = self.fragment_shader.get_fragments()
   

    """Fragment Processing functions in program"""
    def enable_test(self, mode):
        #if test is enabled, fragment processing happens hence create object, else there is no need
        if self.frag_processing == None:
            self.frag_processing = Fragment_Processing(None, self.buffer)
        self.frag_processing.set_test(mode, True)
        
    def disable_test(self, mode):
        self.frag_processing.set_test(mode, False)

    #runs fragment processing stage and sets pixels directly in buffer
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

    def clear_color(self, color):
        self.buffer.draw(color)
        self.buffer.set_alpha(round(color[3]*255, 2))
 