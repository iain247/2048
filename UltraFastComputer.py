# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:29:58 2020

@author: iainr
"""

import random #tensorflow
from UltraFastBoard import UltraFastBoard

brd = UltraFastBoard()

allDirections = ["up","down","right","left"]

showBoard = True
count = 1

while True:
        
    if showBoard:     
        print(count)
    
    direction = random.choice(allDirections)
    
    if direction == "up":
        if showBoard:
            brd.printBoard()
        if brd.moveUp():
            brd.createNewBlock()
            brd.gameStatus()

            
    elif direction == "down":
        if showBoard:
            brd.printBoard()
        if brd.moveDown():
            brd.createNewBlock() 

    
    elif direction == "left":
        if showBoard:
            brd.printBoard()
        if brd.moveLeft():
            brd.createNewBlock()

    
    elif direction == "right":
        if showBoard:
            brd.printBoard()
        if brd.moveRight():
            brd.createNewBlock()
            
            
    count += 1
    


            
    
                