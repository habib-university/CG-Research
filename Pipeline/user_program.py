#Do not remove these imports!!
from fragment_shader import Fragment_Shader
from helpers import screen_resolution

def init():
    #declare global screen variables
    global WIDTH, HEIGHT, block_size, margin
    WIDTH, HEIGHT, block_size, margin = screen_resolution(10, 10) 
    
def render(program):
    #draw the primitives you want in your image
    program.draw_arrays("LINE", 0, 8)

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    program.enable_test('alpha')
    program.enable_test('depth')
    program.alpha_func('GEQUAL', 0.8)
    program.depth_func()
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #blue line is not rendered and magenta line is on top of cyan (due to depth test)
    vertices = [[0,0,0], [5,5,0], [5,0,0], [0,8,0], [4,9,0.5], [4,0,0.5], [2,9,0], [2,0,0]]
    program.send_vertices_data(vertices)
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1], [1,0,1,1], [0,1,1,1], [0,1,1,1], [0,0,1,0.5], [0,0,1,0.5]]
    program.send_color_data(colors)
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor   
