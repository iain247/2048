# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:29:58 2020

@author: iainr
"""

import pygame, sys, time, random#, tensorflow
from Board import Board

brd = Board()
brd.frameRate = 1

allDirections = ["up","down","right","left"]


while True:
       
    for event in pygame.event.get():
        
        #quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()                                
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            pos = pygame.mouse.get_pos()           
            if brd.resetButton.collidepoint(pos):
                brd.reset()
                   
    if not brd.status:
        pygame.event.pump()
        brd.reset()
    
    direction = random.choice(allDirections)
    
    if direction == "up":
        if brd.moveUp():
            brd.createNewBlock()   
            
            
    elif direction == "down":
        if brd.moveDown():
            brd.createNewBlock()
            
    
    elif direction == "left":
        if brd.moveLeft():
            brd.createNewBlock()
            
    
    elif direction == "right":
        if brd.moveRight():
            brd.createNewBlock() 

            
    
                