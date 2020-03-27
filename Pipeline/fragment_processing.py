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
from operator import sub
from framebuffer import Framebuffer
from constants import *

class Fragment_Processing:
    def __init__(self, fragments, frame_buffer):
        self.fragments = fragments #an array of fragments
        self.frame_buffer = frame_buffer
        self.alpha_test = False
        self.blending = False
        self.depthTest = False
##    def pixel_ownership_test(self):
         
    def alpha_func(self, const, ref_val):
        if not self.alpha_test:
            return 'Alpha test not enabled'
        if const == 'GL_ALWAYS':
            return True
        elif const == 'GL_NEVER':
            return False
        elif const == 'GL_LESS':
            for i in range(len(fragments)):
                alpha_val = fragments[i].color[3] #alpha value of each fragment
                if alpha_val >= ref_val:
                    self.fragments.remove(fragments[i]) #did not pass
        elif const == 'GL_LEQUAL':
            for i in range(len(fragments)):
                alpha_val = fragments[i].color[3] #alpha value of each fragment
                if alpha_val > ref_val:
                    self.fragments.remove(fragments[i]) #did not pass
        elif const == 'GL_GEQUAL':
            for i in range(len(fragments)):
                alpha_val = fragments[i].color[3] #alpha value of each fragment
                if alpha_val < ref_val: #if less, did not pass, else pass
                    self.fragments.remove(fragments[i])
        elif const == 'GL_GREATER':
            for i in range(len(fragments)):
                alpha_val = fragments[i].color[3] #alpha value of each fragment
                if alpha_val <= ref_val: #if less or equal, did not pass, else pass
                    self.fragments.remove(fragments[i]) 
        elif const == 'GL_EQUAL':
            for i in range(len(fragments)):
                alpha_val = fragments[i].color[3] #alpha value of each fragment
                if alpha_val != ref_val:
                    self.fragments.remove(fragments[i]) #did not pass
        elif const == 'GL_NOTEQUAL':
            for i in range(len(fragments)):
                alpha_val = fragments[i].color[3] #alpha value of each fragment
                if alpha_val == ref_val:
                    self.fragments.remove(fragments[i]) #did not pass
        else:
            return 'Invalid value'
        return self.fragments
            
    def blend_func(self, src, dst):
        for i in range(len(self.fragments)):
            src_factor = src_blendfactor(src, self.fragments[i])
            dst_factor = dst_blendfactor(dst, self.fragments[i])
            ###constant color for application specified colors
            ###from programmable fragment shader
            self.fragments[i] = (src_factor * self.fragments[i]) +(dst_factor * self.frame_buffer.get_buffer()[i])
        
    def src_blendfactor(self, src, frag):
        if src == 'GL_ZERO':
            src_blend_factor = [0,0,0,0]
        elif src == 'GL_ONE':
            src_blend_factor = [1,1,1,1]
        elif src == 'GL_SRC_ALPHA':
            src_blend_factor = [frag.color[3], frag.color[3],
                                frag.color[3], frag.color[3]]
        elif src == 'GL_ONE_MINUS_SRC_ALPHA':
            src_alpha = [frag.color[3], frag.color[3],
                         frag.color[3], frag.color[3]]
            src_blend_factor = map(sub, [1,1,1,1], src_alpha)
        elif src == 'GL_DST_ALPHA':
            src_blend_factor = [self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3]]
        elif src == 'GL_ONE_MINUS_DST_ALPHA':
            dst_alpha = [self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3],
                            self.frame_buffer.get_buffer()[i][3]]
            src_blend_factor = map(sub, [1,1,1,1], dst_alpha)
        elif src == 'GL_DST_COLOR':
            src_blend_factor = self.frame_buffer.get_buffer()[i]
        elif src == 'GL_ONE_MINUS_DST_COLOR':
            src_blend_factor = map(sub, [1,1,1,1], self.frame_buffer.get_buffer()[i])
        elif src == 'GL_SRC_ALPHA_SATURATE':
            f = min(frag[3], 1 - self.frame_buffer.get_buffer()[i][3])
            src_blend_factor = [f, f, f, 1]
        return src_blend_factor

    def dst_blendfactor(self, dst, frag):
        if dst == 'GL_SRC_COLOR':
            dst_blend_factor = frag.color[3]
        elif dst == 'GL_ONE_MINUS_SRC_COLOR':
            dst_blend_factor = map(sub, [1,1,1,1], frag.color[3])
        elif dst == 'GL_ZERO':
            dst_blend_factor = [0,0,0,0]
        elif dst == 'GL_ONE':
            dst_blend_factor = [1,1,1,1]
        elif dst == 'GL_SRC_ALPHA':
            dst_blend_factor = [frag.color[3], frag.color[3],frag.color[3], frag.color[3]]
         elif dst == 'GL_ONE_MINUS_SRC_ALPHA':
            src_alpha = [frag.color[3], frag.color[3], frag.color[3], frag.color[3]]
            dst_blend_factor = map(sub, [1,1,1,1], src_alpha)
        elif dst == 'GL_DST_ALPHA':
            dst_blend_factor = [self.frame_buffer.get_buffer()[i][3],
                                self.frame_buffer.get_buffer()[i][3],
                                self.frame_buffer.get_buffer()[i][3],
                                self.frame_buffer.get_buffer()[i][3]]
        elif dst == 'GL_ONE_MINUS_DST_ALPHA':
            dst_alpha = [self.frame_buffer.get_buffer()[i][3],
                        self.frame_buffer.get_buffer()[i][3],
                        self.frame_buffer.get_buffer()[i][3],
                        self.frame_buffer.get_buffer()[i][3]]
            dst_blend_factor = map(sub, [1,1,1,1], dst_alpha)
        return dst_blend_factor

    
    def depth_test(self,func):
        ##calculate corresponding depth buffer val
        if not self.depthTest:
            return 'Depth test not enabled'
        if func == 'GL_ALWAYS':
            return True
        elif func == 'GL_NEVER':
            return False
        elif func == 'GL_LESS':
            for i in range(len(fragments)):
                if fragments[i].depth > self.framebuffer.depthBuffer[pos[0]][pos[1]]:
                    self.fragments.remove(fragments[i])
        else:
            return 'Invalid value'
        return self.fragments
    
    def get_fragments(self):
        return self.fragments
    
    def setDepthValue(self, pos, val):
        if self.depthTest == True:
            self.framebuffer.depthBuffer[pos[0]][pos[1]] = val
        else:
            print("unable to write to buffer")
