import pygame
import sys
import time
import threading, queue
from framebuffer import Framebuffer
from constants import *
dblBufferOn = False
pixelOwnershipTestOn = False
scissorTestOn = False
alphaTestOn = False
stencilTestOn = False
depthBufferTestOn = False

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

if __name__=='__main__':
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Grid")

    #initialize variables
    width = height = 20
    margin = 5
    running = True
    refresh = False
    switch = False
    q = queue.Queue()
    
    frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)
    p0 = threading.Thread(target=refresh_buffer, name="r", args=(refresh, frame_buffer, ))
    p1 = threading.Thread(target=frame_buffer.draw, name="r", args=(white,))
    while running:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    dblBufferOn = True
                    # dblBufferOn = not dblBufferOn
                    frame_buffer.enable_doubleBuffering()
                elif event.key == pygame.K_f:
                    pixelOwnershipTestOn = True
                    print("PO test enabled")
                    # enable pixel ownership test
                elif event.key == pygame.K_g:
                    if (pixelOwnershipTestOn==True):
                        scissorTestOn = True
                        #enable scissor test
                        print("scissor test enabled")
                    else:
                        print("pixel ownership test not enabled: press g")
                elif event.key == pygame.K_h:
                    if (scissorTestOn==True):
                        alphaTestOn = True
                        #enable alpha test
                        print("alpha test enabled")
                    else:
                        print("scissor test not enabled: press h")
                elif event.key == pygame.K_j:
                    if (alphaTestOn==True):
                        stencilTestOn = True
                        #enable stencil test
                        print("stencil test enabled")
                    else:
                        print("alpha test not enabled: press j")
                elif event.key == pygame.K_k:
                    if (stencilTestOn==True):
                        depthBufferTestOn = True
                        #enable depth buffer test
                        print("depth buffer test enabled")
                    else:
                        print("stencil test not enabled: press k")
        if not p0.is_alive():
            p0.start()
            p0.join(0.016)
        if not p1.is_alive():
            p1.start()
            p1.join(0.058)
        
        refresh = q.get()
        if p0.is_alive():
            p0.join()
        p0 = threading.Thread(target=refresh_buffer, name="r", args=(refresh, frame_buffer,))

        if p1.is_alive():
            p1.join()
        elif not p1.is_alive() and frame_buffer.buffer_status:
            frame_buffer.set_buffer(refresh)

        if switch:
            p1 = threading.Thread(target=frame_buffer.draw_loops, name="Foo", args=(red,))
            switch = False
        elif not switch:
            p1 = threading.Thread(target=frame_buffer.draw, name="r", args=(white,))
            switch = True

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
