import asyncio
import pygame
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import subprocess
import sys
import time
import threading, queue
from framebuffer import Framebuffer
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
                    frame_buffer.enable_doubleBuffering()

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
