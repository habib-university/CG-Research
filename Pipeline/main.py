import pygame
import sys
import time
import threading, queue
import numpy as np
import user_program
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


if __name__=='__main__':

    #init user program
    user_program.init()
    WIDTH, HEIGHT, block_size, margin = user_program.WIDTH, user_program.HEIGHT, user_program.block_size, user_program.margin
    set_screen_constants(WIDTH, HEIGHT, block_size, margin)

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

    program = Program(screen, frame_buffer, blank_frags)
    user_program.main_program(program)
    program.run_fragment_shader()
    frags = program.get_fragments()
    program.run_fragProcessing(frags)

    pygame.surfarray.blit_array(s, frame_buffer.get_buffer())
    np.copyto(alpha_values, frame_buffer.get_alpha())
    del alpha_values
    screen.blit(s, (0,0))
    
    #Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    frame_buffer.enable_doubleBuffering()

##If the refresh thread is not enabled then uncomment below line
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
