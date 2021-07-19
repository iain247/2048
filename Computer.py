# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:29:58 2020

@author: iainr
"""

import pygame, sys, time, random#, tensorflow
from Board import Board

brd = Board()

allDirections = ["up","down","right","left"]


while True:
    
    keyPress = True
    
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
        time.sleep(3)
        brd.reset()
    
    direction = random.choice(allDirections)
    
    if direction == "up":
        keyPress = False
        if brd.moveUp():
            brd.createNewBlock()
            brd.gameStatus()   
            time.sleep(0.1)
            
    elif direction == "down":
        keyPress = False
        if brd.moveDown():
            brd.createNewBlock()
            brd.gameStatus() 
            time.sleep(0.1)
    
    elif direction == "left":
        keyPress = False
        if brd.moveLeft():
            brd.createNewBlock()
            brd.gameStatus() 
            time.sleep(0.1)
    
    elif direction == "right":
        keyPress = False
        if brd.moveRight():
            brd.createNewBlock()
            brd.gameStatus() 
            time.sleep(0.1)
            
    
                