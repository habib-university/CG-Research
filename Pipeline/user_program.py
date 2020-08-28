from fragment_shader import Fragment_Shader
from helpers import screen_resolution

def init():
    #declare variables
    global WIDTH, HEIGHT, block_size, margin
    WIDTH, HEIGHT, block_size, margin = screen_resolution(10, 10) 

def render(program, fragments=None):
    #blending = blend, depth test = depth, alpha test = alpha
    program.draw_arrays("LINE", 0, 4)

def main_program(program):
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    vertices = [(0,0,0), (5,5,0), (9,0,0), (9,7,0)]
    program.send_vertices_data(vertices)
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1], [1,0,1,1]]
    program.send_color_data(colors)
    render(program)
  
def write_fragmentShader(fragColor, vColor, uniforms = None):
    #varying vColor
    #uniform something
    #frag_color = vColor

    #there may be other components in this program after shading and texture etc which sets colors
    #differently. For now we just assign color

    fragColor = vColor
    #fragColor = [1, 0, 0, 1] #red

    return fragColor