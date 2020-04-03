"""
    There maybe multiple fragments generated for a pixel if there is
    multisampling or the use of textures. For our purposes here, we are
    assuming there are no samplers or textures, so one fragment represents
    one pixel.

    In this case, fragment = pixel (which is how it is in OpenGL. In WebGL,
    there are different objects for fragment and pixel. However,
    they're almost the same, with the exception of some attributes.

    Alpha test is implemented, however it is deprecated in webGL.
    Similar functionality can be obtained by adding conditionals in the
    fragment shader.
"""
from operator import add, sub, mul
from framebuffer import Framebuffer
from constants import *

class Fragment_Processing:
    def __init__(self, fragments, frame_buffer):
        self.fragments = fragments #an array of fragments
        self.frame_buffer = frame_buffer
        self.alpha_test = False
        self.blending = False
        self.depth_test = False
##    def pixel_ownership_test(self):
         
    def alpha_func(self, const, ref_val): #ref val will be between 0-255
        if not self.alpha_test:
            return 'Alpha test not enabled'
        for i in range(len(self.fragments)):
            if const == 'ALWAYS':
                continue
            elif const == 'NEVER':
                self.fragments[i].color = black
            elif const == 'LESS':
                alpha_val = self.fragments[i].color[3] #alpha value of each fragment
                if alpha_val >= ref_val:
                    #self.fragments.remove(fragments[i]) #did not pass
                    self.fragments[i].color = black
            elif const == 'LEQUAL':
                alpha_val = self.fragments[i].color[3] #alpha value of each fragment
                if alpha_val > ref_val:
                    #self.fragments.remove(fragments[i]) #did not pass
                    self.fragments[i].color = black
            elif const == 'GEQUAL':
                alpha_val = self.fragments[i].color[3] #alpha value of each fragment
                if alpha_val < ref_val: #if less, did not pass, else pass
                    #self.fragments.remove(fragments[i])
                    self.fragments[i].color = black
            elif const == 'GREATER': #if frag value is greater than ref value, pass
                alpha_val = self.fragments[i].color[3] #alpha value of each fragment
                if alpha_val <= ref_val: #if less or equal, did not pass, else pass
                    #self.fragments.remove(fragments[i])
                    self.fragments[i].color = black
            elif const == 'EQUAL':
                alpha_val = self.fragments[i].color[3] #alpha value of each fragment
                if alpha_val == ref_val:
                    #self.fragments.remove(fragments[i]) #did not pass
                    self.fragments[i].color = black
            elif const == 'NOTEQUAL':
                alpha_val = self.fragments[i].color[3] #alpha value of each fragment
                if alpha_val != ref_val:
                    #self.fragments.remove(fragments[i]) #did not pass
                    self.fragments[i].color = black
            else:
                return 'Invalid value'
        return self.fragments
            
    def blend_func(self, src, dst):
        for i in range(len(self.fragments)):
            src_factor = self.src_blendfactor(src, self.fragments[i])
            dst_factor = self.dst_blendfactor(dst, self.fragments[i])
            ###constant color for application specified colors
            ###from programmable fragment shader
            ind = self.fragments[i].buffer_pos
            sf = list(map(mul,src_factor, self.fragments[i].color))
            df = list(map(mul, dst_factor, self.frame_buffer.get_buffer()[ind[0]][ind[1]]))
            self.fragments[i].color = list(map(add, sf, df))
        
    def src_blendfactor(self, src, frag):
        if src == 'ZERO':
            src_blend_factor = [0,0,0,0]
        elif src == 'ONE':
            src_blend_factor = [1,1,1,1]
        elif src == 'SRC_ALPHA':
            src_blend_factor = [frag.color[3], frag.color[3],
                                frag.color[3], frag.color[3]]
        elif src == 'ONE_MINUS_SRC_ALPHA':
            src_alpha = [frag.color[3], frag.color[3],
                         frag.color[3], frag.color[3]]
            src_blend_factor = list(map(sub, [1,1,1,1], src_alpha))
        elif src == 'DST_ALPHA':
            src_blend_factor = [self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3]]
        elif src == 'ONE_MINUS_DST_ALPHA':
            dst_alpha = [self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3]]
            src_blend_factor = list(map(sub, [1,1,1,1], dst_alpha))
        elif src == 'DST_COLOR':
            src_blend_factor = self.frame_buffer.get_buffer()[i]
        elif src == 'ONE_MINUS_DST_COLOR':
            src_blend_factor = list(map(sub, [1,1,1,1], self.frame_buffer.get_buffer()[i]))
        elif src == 'SRC_ALPHA_SATURATE':
            f = min(frag[3], 1 - self.frame_buffer.get_buffer()[i][3])
            src_blend_factor = [f, f, f, 1]
        return src_blend_factor

    def dst_blendfactor(self, dst, frag):
        if dst == 'SRC_COLOR':
            dst_blend_factor = frag.color[3]
        elif dst == 'ONE_MINUS_SRC_COLOR':
            dst_blend_factor = list(map(sub, [1,1,1,1], frag.color[3]))
        elif dst == 'ZERO':
            dst_blend_factor = [0,0,0,0]
        elif dst == 'ONE':
            dst_blend_factor = [1,1,1,1]
        elif dst == 'SRC_ALPHA':
            dst_blend_factor = [frag.color[3], frag.color[3],
                                frag.color[3], frag.color[3]]
        elif dst == 'ONE_MINUS_SRC_ALPHA':
            src_alpha = [frag.color[3], frag.color[3],
                        frag.color[3], frag.color[3]]
            dst_blend_factor = list(map(sub, [1,1,1,1], src_alpha))
        elif dst == 'DST_ALPHA':
            dst_blend_factor = [self.frame_buffer.get_buffer()[i][3],
                                self.frame_buffer.get_buffer()[i][3],
                                self.frame_buffer.get_buffer()[i][3],
                                self.frame_buffer.get_buffer()[i][3]]
        elif dst == 'ONE_MINUS_DST_ALPHA':
            dst_alpha = [self.frame_buffer.get_buffer()[i][3],
                        self.frame_buffer.get_buffer()[i][3],
                        self.frame_buffer.get_buffer()[i][3],
                        self.frame_buffer.get_buffer()[i][3]]
            dst_blend_factor = list(map(sub, [1,1,1,1], dst_alpha))
        return dst_blend_factor

    
    def depth_func(self):
        if self.depth_test == False:
            return "Depth Test not Enabled"
        else:
            for i in range(len(self.fragments)):
                if (self.fragments[i].depth < self.frame_buffer.getdepthBuffer()[self.fragments[i].buffer_pos[1]][self.fragments[i].buffer_pos[0]]):
                    self.frame_buffer.set_depth(self.fragments[i].buffer_pos,self.fragments[i].depth, self.fragments[i].color)
                    
    def get_fragments(self):
        return self.fragments
