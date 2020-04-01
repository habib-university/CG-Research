import pygame
import sys
import time
import threading, queue
import numpy as np
from framebuffer import Framebuffer
from fragment_processing import *
from fragment_shader import *
from constants import *

"""
    This file contains the code for main program running the graphics pipeline.
"""
    
def refresh_buffer(r, buffer):
    if r:
        refresh = False
    elif not r:
        refresh = True
    q.put(refresh)
    pygame.surfarray.blit_array(screen, buffer.get_buffer())   
    pygame.display.update()

def buffer_to_fragments(buf):
    fragments = []
    for i in range(len(buf)):
        for j in range(len(buf[i])):
            color = [buf[i][j][0], buf[i][j][1], buf[i][j][2], alpha_values[i][j]]
            fragments.append(Fragment(color, [i,j]))
    return fragments
            
def change_alpha(val):
    temp = np.zeros((255, 255), dtype=alpha_values.dtype)
    for i in range(len(val)):
        for j in range(len(val[i])):
            temp[i][j] = 100
    return temp

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
    q = queue.Queue()
    frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)
    alpha_values = []

    #thread for refreshing and switching buffers
    p0 = threading.Thread(target=refresh_buffer, name="r", args=(refresh, frame_buffer, ))
    p1 = threading.Thread(target=frame_buffer.draw, name="r", args=(white,))
    
    #Below line is used only if screen switch is disabled
    frame_buffer.draw(green)

    alpha = True
    alpha_values = pygame.surfarray.pixels_alpha(s)
    frags = buffer_to_fragments(frame_buffer.get_buffer())

    #fragment shader
    fragment_shader = Fragment_Shader(frags)
    fragment_shader.set_fragColor([255,0,0,126]) #red with low opacity
    fragment_shader.run_shader()
    
    #program
    program = Program(screen, frame_buffer)
    program.attach_shader(fragment_shader)
    program.enable_test('blend')
    #program.frag_processing.alpha_func('EQUAL', 255) 
    program.frag_processing.blend_func('SRC_ALPHA', 'ONE_MINUS_SRC_ALPHA')
    program.send_fragments()    
    
    #main loop
    while running:
        #s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    frame_buffer.enable_doubleBuffering()

        pygame.surfarray.blit_array(s, frame_buffer.get_buffer())
        if not alpha:
            alpha_values = pygame.surfarray.pixels_alpha(s)
            alpha = True
        if alpha:
            temp = change_alpha(alpha_values)
            np.copyto(alpha_values, temp)
            del alpha_values
            alpha = False
        screen.blit(s, (0,0))
        
        pygame.display.update()

        if not p0.is_alive():
            p0.start()
            p0.join(0.016)
            
##Comment p1 thread if screen switch disabled
##        if not p1.is_alive():
##            p1.start()
##            p1.join(0.058)
        
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




    """
    I have not yet combined the fragment processing and fragment shader
    code with the main file. This is just an overview of how it should
    be in main.py file.

    
    frag_shader = Fragment_Shader(frags)
    frag_shader.set_fragColor([255,0,0,1])
    frag_shader.run_shader()
    program = Program()
    program.attach_shader(fragment_shader)
    #by default, all the fragment processing operations are disabled.
    program.draw()
    """
