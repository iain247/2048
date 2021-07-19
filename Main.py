# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:20:48 2020

@author: iainr
"""

import pygame, sys, time
from Board import Board

###########################################
## BUGS 
## IF BOARD FILLS, IT RANDOMLY MOVES TO CHECK, STOP THIS!!
## MAKE IT CHECK IF IT CAN MOVE WITHOUT ACTUALLY MOVING THE BLOCKS
##
## FIXED THIS, MAKE CHANGES ON OTHER FILES
##
## TRY OPTIMISE CODE!!


## CHANGES MADE TO BOARD WHICH SHOULD BE MADE TO OTHER BOARDS
# SIMPLIFIED GETCOORD
# UPDATE BOARD FOR LOOP REMOVED AND REPLACED WITH COPY



#create board class
brd = Board()

while True:
    
    keyPress = True
            
    for event in pygame.event.get():
        
        #quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()        
        
        #handle key presses
        if event.type == pygame.KEYDOWN and keyPress:
            
            if event.key == pygame.K_UP:
                if brd.moveUp():
                    brd.createNewBlock() 
                    time.sleep(0.1)
                keyPress = False
                                                     
            
            elif event.key == pygame.K_DOWN:
                if brd.moveDown():
                    brd.createNewBlock()
                    time.sleep(0.1)
                keyPress = False
            
                
            elif event.key == pygame.K_LEFT:
                if brd.moveLeft():
                    brd.createNewBlock()
                    time.sleep(0.1)
                keyPress = False
                    
                
            elif event.key == pygame.K_RIGHT:
                if brd.moveRight():
                    brd.createNewBlock()
                    time.sleep(0.1)
                keyPress = False
                        
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            pos = pygame.mouse.get_pos()           
            if brd.resetButton.collidepoint(pos):
                brd.reset()
                