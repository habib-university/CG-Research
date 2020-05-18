import pygame
import sys
import time
import threading, queue
import numpy as np
from framebuffer import Framebuffer
from fragment_shader import *
from program import *
from constants import *
from helpers import *

"""
    This file contains the code for main program running the graphics pipeline.
"""

def refresh_buffer(r, buffer):
    if r:
        refresh = False
    elif not r:
        refresh = True
    q.put(refresh)
    screen.fill((0,0,0,255))
    alpha = pygame.surfarray.pixels_alpha(s)
    pygame.surfarray.blit_array(s, buffer.get_buffer())
    np.copyto(alpha, buffer.get_alpha())
    del alpha
    screen.blit(s, (0,0))
    pygame.display.update()  

def buffer_to_fragments(buf, depth):
    fragments = []
    for i in range(len(buf)):
        for j in range(len(buf[i])):
            color = [buf[i][j][0], buf[i][j][1], buf[i][j][2], alpha_values[i][j]]
            fragments.append(Fragment(color, [i,j,depth]))
    return fragments

def render(program, fragments=None):
    #blending = blend, depth test = depth, alpha test = alpha

    render.fragments = fragments #do not change this line!

    render.fragments = draw_point(program, 2, 0, 0, [1.0, 0.0, 0.0, 1])#red color point
    render.fragments = draw_point(program, 2, 1, 0, [1.0, 0.0, 0.0, 0.9])
    render.fragments =draw_point(program, 2, 2, 0, [1.0, 0.0, 0.0, 0.8])
    render.fragments =draw_point(program, 2, 3, 0, [1.0, 0.0, 0.0, 0.7])
    render.fragments =draw_point(program, 2, 4, 0, [1.0, 0.0, 0.0, 0.6])
    render.fragments =draw_point(program, 2, 5, 0, [1.0, 0.0, 0.0, 0.5])
    render.fragments =draw_point(program, 2, 6, 0, [1.0, 0.0, 0.0, 0.4])#red color point
    render.fragments =draw_point(program, 2, 7, 0, [1.0, 0.0, 0.0, 0.3])
    render.fragments =draw_point(program, 2, 8, 0, [1.0, 0.0, 0.0, 0.2])
    render.fragments =draw_point(program, 2, 9, 0, [1.0, 0.0, 0.0, 0])
    
    return render.fragments

def render2(program, fragments=None):
    render.fragments = fragments #do not change this line!

    program.enable_test('blend')
    render.fragments =draw_point(program, 2, 9, 0, [0.0, 1.0, 0.0, 1])
    render.fragments =draw_point(program, 2, 8, 0, [0.0, 1.0, 0.0, 0.9])
    render.fragments =draw_point(program, 2, 7, 0, [0.0, 1.0, 0.0, 0.8])
    render.fragments =draw_point(program, 2, 6, 0, [0.0, 1.0, 0.0, 0.7])
    render.fragments =draw_point(program, 2, 5, 0, [0.0, 1.0, 0.0, 0.6]) #green color point
    render.fragments =draw_point(program, 2, 4, 0, [0.0, 1.0, 0.0, 0.5])
    render.fragments =draw_point(program, 2, 3, 0, [0.0, 1.0, 0.0, 0.4])
    render.fragments =draw_point(program, 2, 2, 0, [0.0, 1.0, 0.0, 0.3])
    render.fragments =draw_point(program, 2, 1, 0, [0.0, 1.0, 0.0, 0.2])
    render.fragments =draw_point(program, 2, 0, 0, [0.0, 1.0, 0.0, 0])
    
    program.blend_func('SRC_ALPHA', 'ONE_MINUS_SRC_ALPHA')
    return render.fragments
            
def draw_point(prog, x, y, z, color):
    fragments = render.fragments
    new_coord = coordinate_conversion(x,y, block_size, margin)
    x = new_coord[0]
    y = new_coord[1]
    x_Limit = x + block_size
    y_Limit = y + block_size
    for i in range(len(fragments)):
        x_pos = fragments[i].buffer_pos[0]
        y_pos = fragments[i].buffer_pos[1]
        
        if (x_pos >= x and x_pos <= x_Limit) and (y_pos >= y and y_pos <= y_Limit):
            if fragments[i].color == [255, 255, 255, 255] or fragments[i].color == [1,1,1,1]:
                fragments[i].color = color
                fragments[i].depth = z
            else:
                pos = [fragments[i].buffer_pos[0], fragments[i].buffer_pos[1], z]
                fragments.append(Fragment(color, pos))
        else:
            color_bool = check_255(fragments[i].color)
            if color_bool:
                new_color = convert_01(fragments[i].color)
                fragments[i].color = new_color
    return fragments

def write_fragmentShader(fragColor, vColor, uniforms = None):
    #varying vColor
    #uniform something
    #frag_color = vColor

    #there may be other components in this program after shading and texture etc which sets colors
    #differently. For now we just assign color

    fragColor = vColor

    return fragColor

if __name__=='__main__':

    #screen_resolution(width, height)
    WIDTH, HEIGHT, block_size, margin = screen_resolution(20, 10) 

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Grid")
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    
    #initialize variables
    running = True
    refresh = False
    switch = False
    d = 0
    q = queue.Queue()
    frame_buffer = Framebuffer(block_size, margin, WIDTH, HEIGHT)

    #thread for refreshing and switching buffers
    p0 = threading.Thread(target=refresh_buffer, name="r", args=(refresh, frame_buffer, ))
    #p1 = threading.Thread(target=frame_buffer.draw, name="r", args=(white,))
    
    #Below three lines are uncommented only if screen switch is disabled
    frame_buffer.draw(white)
    pygame.surfarray.blit_array(s, frame_buffer.get_buffer())
    pygame.display.update()
    
    #get array for alpha values and fragments as input
    alpha_values = pygame.surfarray.pixels_alpha(s)
    blank_frags = buffer_to_fragments(frame_buffer.get_buffer(), d)

    program = Program(screen, frame_buffer)
    frags = render(program, blank_frags)
    fragment_shader = Fragment_Shader(blank_frags)
    program.attach_shader(fragment_shader)
    frags = fragment_shader.run_shader(frags, write_fragmentShader)
    program.run_fragProcessing(frags)

    #if we want to use blending
    #frags = render2(program, blank_frags)
    #frags = fragment_shader.run_shader(frags, write_fragmentShader)
    #program.run_fragProcessing(frags)

    pygame.surfarray.blit_array(s, frame_buffer.get_buffer())
    np.copyto(alpha_values, frame_buffer.get_alpha())
    del alpha_values
    screen.blit(s, (0,0))
    
    #main loop
    while running:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    frame_buffer.enable_doubleBuffering()

        # if the refresh thread is not enabled then uncomment below line
##        pygame.display.update()

        if not p0.is_alive():
            p0.start()
            p0.join(0.016)
            
##Comment p1 thread if screen switch disabled
##        if not p1.is_alive():
##            p1.start()
##            p1.join(0.058)
##        
        refresh = q.get()
        if p0.is_alive():
            p0.join()
        p0 = threading.Thread(target=refresh_buffer, name="r", args=(refresh, frame_buffer,))
        
##Comment the code below (before quit) if you want to disable screen switch
##        if p1.is_alive():
##            p1.join()
##        elif not p1.is_alive() and frame_buffer.buffer_status:
##            frame_buffer.set_buffer(refresh)
##
##        if switch:
##            p1 = threading.Thread(target=frame_buffer.draw_loops, name="Foo", args=(red,))
##            switch = False
##        elif not switch:
##            p1 = threading.Thread(target=frame_buffer.draw, name="r", args=(white,))
##            switch = True

    pygame.quit()
