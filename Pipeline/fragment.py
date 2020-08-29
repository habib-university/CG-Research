"""
    This file implements the fragment class.

    Note:
    There maybe multiple fragments generated for a pixel if there is
    multisampling or if textures are used. For our purposes here, we are
    assuming there are no samplers or textures, so one fragment represents
    one pixel.
    In this case, fragment = pixel. (which is how it is in OpenGL. In WebGL,
    there are different objects for fragment and pixel.) However,
    they're almost the same, with the exception of some attributes.
"""

class Fragment:
    def __init__(self, color, buffer_pos):
        """
            Position will be a vec3 = (x,y,z) and color will be vec4 = (R,G,B,A)
            The interpolated attributes in the fragment includes color and
            texture. Right now we're only considering color.
        """
        self.buffer_pos = buffer_pos  #position of fragment/pixel in buffer
        self.color = color  
        self.depth = buffer_pos[2] #depth = z
        self.is_color = False #bool to specify if this fragment should be colored or not
