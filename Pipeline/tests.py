
"""Test 1: Drawing simple points with colors"""
def render(program):
    #blending = blend, depth test = depth, alpha test = alpha
    program.draw_arrays("POINT", 0, 6)

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    vertices = [(2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0)]
    program.send_vertices_data(vertices)
    colors = [[1,0,0,1], [0,1,0,1], [0,0,1,1], [1,1,0,1], [0,1,1,1], [1,0,1,1]]
    program.send_color_data(colors)
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 2: Drawing simple points with color specified directly in fragment shader"""
def render(program):
    #blending = blend, depth test = depth, alpha test = alpha
    program.draw_arrays("POINT", 0, 6)

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    vertices = [(2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0)]
    program.send_vertices_data(vertices)
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = [1,0,0,1]  #Red
    return fragColor

"""Test 3: Drawing simple points with depth test"""
def render(program):
    program.draw_arrays("POINT", 0, 6)

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    #enable depth test
    program.enable_test('depth')
    program.depth_func()
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #vertex with lower z-value should come on top i.e. Red, yellow and blue pixels should be visible
    vertices = [[2, 0, 0], [2, 0, 1], [3, 0, 0.5], [3, 0, 1], [4, 0, 1], [4, 0, 0]]
    program.send_vertices_data(vertices)
    colors = [[1, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1]]
    program.send_color_data(colors)
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 4: Drawing simple points with alpha test"""
def render(program):
    program.draw_arrays("POINT", 0, 6)

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    program.enable_test('alpha')
    program.alpha_func('GEQUAL', 0.5)
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    vertices = [(2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0)]
    program.send_vertices_data(vertices)
    colors = [[1,0,0,0.5], [0,1,0,1], [0,0,1,0.3], [1,1,0,0.4], [0,1,1,0.8], [1,0,1,1]]
    program.send_color_data(colors)
    render(program)
  
def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 5: Drawing simple points with blending"""
def render(program):
    program.disable_test('blend')
    program.draw_arrays("POINT", 0, 9)
    program.enable_test('blend')
    program.draw_arrays("POINT", 10, 20)
    program.blend_func('SRC_ALPHA', 'ONE_MINUS_SRC_ALPHA')

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    program.enable_test('blend')
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    vertices = [(2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0), (2,6,0), (2,7,0), (2,8,0), (2,9,0), (2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0), (2,6,0), (2,7,0), (2,8,0), (2,9,0)]
    program.send_vertices_data(vertices)
    colors = [[1,0,0,1], [1,0,0,0.9], [1,0,0,0.8], [1,0,0,0.7], [1,0,0,0.6], [1,0,0,0.5], [1,0,0,0.4], [1,0,0,0.3], [1,0,0,0.2], [1,0,0,0], [0,1,0,0], [0,1,0,0.2], [0,1,0,0.3], [0,1,0,0.4], [0,1,0,0.5], [0,1,0,0.6], [0,1,0,0.7], [0,1,0,0.8], [0,1,0,0.9], [0,1,0,1]]
    program.send_color_data(colors)
    render(program)
  
def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 6: Drawing lines with colors with red background color"""
def render(program):
    #draw the primitives you want in your image
    program.draw_arrays("LINE", 0, 4)

def main_program(program):
    #specify background color
    program.clear_color([1, 0, 0, 1])
    #attach fragment shader
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #give vertices array
    vertices = [(0,0,0), (5,5,0), (9,0,0), (9,7,0)]
    program.send_vertices_data(vertices)
    #specify colors for each vertex
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1], [1,0,1,1]]
    program.send_color_data(colors)
    #render primitives
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 7: Drawing points and lines"""
def render(program):
    #draw the primitives you want in your image
    program.draw_arrays("LINE", 0, 4)
    program.draw_arrays("POINT", 4, 6)

def main_program(program):
    #specify background color
    program.clear_color([1, 1, 1, 1])
    #attach fragment shader
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #give vertices array
    vertices = [(0,0,0), (5,5,0), (9,0,0), (9,7,0), (9,9,0), (2, 9, 0)]
    program.send_vertices_data(vertices)
    #specify colors for each vertex
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1], [1,0,1,1], [0,0,1,1], [0,1,0,1]]
    program.send_color_data(colors)
    #render primitives
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 8: Drawing points and lines (with points at start/end point of line)"""
def render(program):
    #draw the primitives you want in your image
    program.draw_arrays("LINE", 0, 4)
    program.draw_arrays("POINT", 4, 6)

def main_program(program):
    #specify background color
    program.clear_color([1, 1, 1, 1])
    #attach fragment shader
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #give vertices array
    vertices = [(0,0,0), (5,5,0), (9,0,0), (9,7,0), (9,7,0), (0, 0, 0)]
    program.send_vertices_data(vertices)
    #specify colors for each vertex
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1], [1,0,1,1], [0,0,1,1], [0,1,0,1]]
    program.send_color_data(colors)
    #render primitives
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 9: Drawing line with odd number of points"""
def render(program):
    #draw the primitives you want in your image
    program.draw_arrays("LINE", 0, 3)

def main_program(program):
    #specify background color
    program.clear_color([1, 1, 1, 1])
    #attach fragment shader
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #give vertices array
    vertices = [(0,0,0), (5,5,0), (9,0,0)]
    program.send_vertices_data(vertices)
    #specify colors for each vertex
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1]]
    program.send_color_data(colors)
    #render primitives
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 10: Drawing multiple lines on top of each other"""
def render(program):
    #draw the primitives you want in your image
    program.draw_arrays("LINE", 0, 4)

def main_program(program):
    #specify background color
    program.clear_color([1, 1, 1, 1])
    #attach fragment shader
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    #give vertices array
    vertices = [[0,0,0], [5,5,0], [5,0,0], [0,8,0]]
    program.send_vertices_data(vertices)
    #specify colors for each vertex
    colors = [[1,1,0,1], [1,1,0,1], [1,0,1,1], [1,0,1,1]]
    program.send_color_data(colors)
    #render primitives
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor

"""Test 11: Drawing multiple primitives with alpha + depth test"""
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

"""Test 11: Drawing multiple primitives with alpha + blend test"""
def render(program):
    program.disable_test('blend')
    program.draw_arrays("POINT", 0, 9)
    program.enable_test('blend')
    program.draw_arrays("POINT", 10, 20)
    program.blend_func('SRC_ALPHA', 'ONE_MINUS_SRC_ALPHA')

def main_program(program):
    program.clear_color([1, 1, 1, 1])
    #whatever the order of tests is, alpha test will be performed before blending
    program.enable_test('blend')
    program.enable_test('alpha')
    program.alpha_func('GREATER', 0.3)
    fragment_shader = Fragment_Shader()
    program.attach_shader(fragment_shader)
    vertices = [(2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0), (2,6,0), (2,7,0), (2,8,0), (2,9,0), (2,0,0), (2,1,0), (2,2,0), (2,3,0), (2,4,0), (2,5,0), (2,6,0), (2,7,0), (2,8,0), (2,9,0)]
    program.send_vertices_data(vertices)
    colors = [[1,0,0,1], [1,0,0,0.9], [1,0,0,0.8], [1,0,0,0.7], [1,0,0,0.6], [1,0,0,0.5], [1,0,0,0.4], [1,0,0,0.3], [1,0,0,0.2], [1,0,0,0], [0,1,0,0], [0,1,0,0.2], [0,1,0,0.3], [0,1,0,0.4], [0,1,0,0.5], [0,1,0,0.6], [0,1,0,0.7], [0,1,0,0.8], [0,1,0,0.9], [0,1,0,1]]
    program.send_color_data(colors)
    render(program)

def write_fragmentShader(fragColor, vColor, uniforms = None):
    fragColor = vColor
    return fragColor
