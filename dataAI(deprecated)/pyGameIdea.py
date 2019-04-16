#=============================================================================
# 15-112 Term Project Spring 2019
# Phil Huang
# ID: xiangheh
# Recitation Section: G
#=============================================================================

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#initialize pygame
pygame.init()

def run():
#creates a window of 500 width, 500 height
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("First Game")
    
    x = 50
    y = 50
    width = 40
    height = 60
    vel = 3
    
    run = True
    while run:
        pygame.time.delay(10)
        win.fill((0,0,0)) 
        pygame.draw.rect(win, (255,0,0), (x, y, width, height))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Checks if the red button in the corner of the window is clicked
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0:
            x -= vel
        if keys[pygame.K_RIGHT] and x < 500 - width:
            x += vel
        if keys[pygame.K_UP] and y > 0:
            y -= vel
        if keys[pygame.K_DOWN] and y < 500 - height:
            y += vel
    pygame.quit()
    
run()