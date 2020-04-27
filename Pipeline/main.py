import pygame
import sys
import time
import threading, queue
import numpy as np
from framebuffer import Framebuffer
from fragment_processing import *
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
##    pygame.surfarray.blit_array(screen, buffer.get_buffer())

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

def draw_point(prog, x, y, z, color):
    fragments = prog.fragment_shader.get_fragments()
    x_Limit = x + 20
    y_Limit = y + 20
    for i in range(len(fragments)):
        x_pos = fragments[i].buffer_pos[1]
        y_pos = fragments[i].buffer_pos[0]
        if (x_pos >= x and x_pos <= x_Limit) and (y_pos >= y and y_pos <= y_Limit):
            fragments[i].color = color
            fragments[i].depth = z
        else:
            color_bool = check_255(fragments[i].color)
            if color_bool:
                new_color = convert_01(fragments[i].color)
                fragments[i].color = new_color
    prog.update_fragments(fragments)

if __name__=='__main__':
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Grid")
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    
    #initialize variables
    width = height = 20
    margin = 5
    running = True
    refresh = False
    switch = False
    d = 0
    q = queue.Queue()
    frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)

    #thread for refreshing and switching buffers
    p0 = threading.Thread(target=refresh_buffer, name="r", args=(refresh, frame_buffer, ))
    #p1 = threading.Thread(target=frame_buffer.draw, name="r", args=(white,))
    
    #Below three lines are uncommented only if screen switch is disabled
    frame_buffer.draw(white)
    pygame.surfarray.blit_array(s, frame_buffer.get_buffer())
    pygame.display.update()
    
    #get array for alpha values and fragments as input
    alpha_values = pygame.surfarray.pixels_alpha(s)
    frags = buffer_to_fragments(frame_buffer.get_buffer(), d)

    #fragment shader
    fragment_shader = Fragment_Shader(frags)
    fragment_shader.set_fragColor([255,0,0,255]) 
    fragment_shader.run_shader()

    #program
    program = Program(screen, frame_buffer)
    program.attach_shader(fragment_shader)

#blending = blend, depth test = depth, alpha test = alpha
    program.enable_test('alpha')
    program.enable_test('depth')
    program.enable_test('blend')
    
    draw_point(program, 5, 5, 0, [1.0, 0.0, 0.0, 1])#red color point
##    draw_point(program, 5, 5, 0, [1, 1, 0, 1]) #yellow color point
    
    program.frag_processing.alpha_func('ALWAYS', 0.5)
    program.frag_processing.depth_func()

    draw_point(program, 5, 30, 0, [0, 1, 1, 0.5]) #cyan color point
    program.frag_processing.alpha_func('ALWAYS', 0.5)
    program.frag_processing.depth_func()
    
    draw_point(program, 5, 5, 0, [0.0, 1.0, 0.0, 0.58]) #green color point
    program.frag_processing.alpha_func('ALWAYS', 0.5)
    program.frag_processing.depth_func()
    program.frag_processing.blend_func('SRC_ALPHA', 'ONE_MINUS_SRC_ALPHA')
##
##    program.frag_processing.alpha_func('EQUAL', 1)
##    program.frag_processing.depth_func()

##    draw_point(program, 5, 55, 0.5, [1, 0, 1, 1]) #magenta point
##    program.frag_processing.alpha_func('ALWAYS', 1)
##    program.frag_processing.depth_func()

##    program.frag_processing.blend_func('SRC_ALPHA', 'ONE_MINUS_SRC_ALPHA')
    

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
