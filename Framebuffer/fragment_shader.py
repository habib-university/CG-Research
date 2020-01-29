import asyncio
import pygame
from framebuffer import Framebuffer
from constants import *

"""
    This file contains the code for fragment shader.
"""

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
frame_buffer = Framebuffer(width, height, margin, WIDTH, HEIGHT)
    
async def refresh_buffer(delay, r):
    await asyncio.sleep(delay)
    if r:
        refresh = False
    elif not r:
        refresh = True
    return refresh

async def switch_screen(delay, r):
    await asyncio.sleep(delay)
    if r:
        switch = False
        frame_buffer.draw(white)
    else:
        switch = True
        frame_buffer.draw_face(red)
    frame_buffer.set_buffer(refresh)
    return switch

    
frame_buffer.draw(white)

while running:
    
    loop = asyncio.get_event_loop()
    tasks = refresh_buffer(0.016, refresh), switch_screen(0.05, switch)
    a, b = loop.run_until_complete(asyncio.gather(*tasks))
    refresh = a
    switch = b
    
    # process inputs(events)
    for event in pygame.event.get():
            
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                frame_buffer.enable_doubleBuffering()

    frame_buffer.set_buffer(refresh)
    pygame.surfarray.blit_array(screen, frame_buffer.get_buffer())
        
    pygame.display.update()
    
pygame.quit()
