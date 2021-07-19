# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:12:43 2020

@author: iainr
"""

import random, collections, copy
import numpy as np
from Block import Block

class UltraFastBoard:
    def __init__(self, size=4):
        
        self.size = size
        
        self.score = 0
        self.highScore = 0
        self.bestBlock = 0
        
        self.status = True # game is ongoing
        
        self.allBlocks = []
        self.buffer = []
               
        self.reset()
             
        
    def cellStatus(self, pos):
        """
        Returns true if there is no block in a specific cell
        """
        row, col = pos
        for block in self.allBlocks:
            if row == block.pos[0] and col == block.pos[1]:
                return False
            
        return True
        
    
    def reset(self):
        """
        resets board as well as buffer and list of blocks
        """        
        self.status = True
        self.allBlocks = []
        self.buffer = []
        
        self.score = 0   
            
        self.updateScore()
        self.updateHighScore(self.highScore)
        
        self.createNewBlock()
        self.createNewBlock()
            
         
    def updateScore(self):
        """
        Updates the score of the game.
        """                   
        if self.score >= self.highScore:
            self.updateHighScore(self.score)
            
            
      
    
    def updateHighScore(self, score):
        """
        Updates the highscore
        """       
        self.highScore = score
        
        for block in self.allBlocks:
            if block.value > self.bestBlock:
                self.bestBlock = block.value
        
        
    def updateBoard(self):
        """
        Updates board from the buffer and resets buffer
        Returns true if the board updates
        """       
        #check if board updates
        #use collections so order of list doesn't matter
        if (collections.Counter(self.allBlocks) == 
            collections.Counter(self.buffer)):
                
            self.buffer = [] # reset buffer
            for block in self.allBlocks:
                block.merged = False
            
            return False
            
        self.allBlocks = copy.deepcopy(self.buffer)
            
        self.buffer = []
        
        self.updateScore()
              
        return True
                       
        
    def addBuffer(self, blocks):
        """
        Adds blocks to the list of blocks on the board
        """
        for x in blocks:
            self.buffer.append(x)
                
        
    def createNewBlock(self):
        """
        Creates a new 2 or 4 block at a random position
        """                                 
        startNum = [2,2,2,2,2,2,2,2,2,4] # 10% chance of a 4

        value = random.choice(startNum)
        
        while True:
            pos = [random.randint(0,3), random.randint(0,3)]
            if self.cellStatus(pos):
                break
                
        newBlock = Block(value, pos)
        
        self.allBlocks.append(newBlock)
        
        if len(self.allBlocks) == self.size**2:
            self.gameStatus()
        
        
    def gameStatus(self):       
        """
        Sets the game status to false if there are no available moves
        """              
        for i in range(self.size):
        
            row = [block for block in self.allBlocks if block.pos[0] == i]
    
            row.sort(key=lambda x: x.pos[1]) # sort based on block.position (columns) 
            
            for block in row:
                block.prevPos = block.pos.copy()
                           
            mergedRow = self.mergeBlocks(row)
            
            if not (collections.Counter(row) == 
                    collections.Counter(mergedRow)): # this line might be wrong, even if row is the same, block objects are different
                return  
              
            col = [block for block in self.allBlocks if block.pos[1] == i]

            col.sort(key=lambda x: x.pos[0])
           
            for block in col:
                block.prevPos = block.pos.copy()                
            
            mergedCol = self.mergeBlocks(col)
            
            if not (collections.Counter(col) == 
                    collections.Counter(mergedCol)):
                return
            
        self.status = False
        self.reset()
 
           
    def moveLeft(self):
        """
        Moves all blocks to the left
        New blocks are stored in the buffer and then updated
        Returns true if a new move is possible
        """
        for i in range(self.size):
            
            row = [block for block in self.allBlocks if block.pos[0] == i]

            row.sort(key=lambda x: x.pos[1]) # sort based on block.position (columns) 
            
            for block in row:
                block.prevPos = block.pos.copy()
                           
            mergedRow = self.mergeBlocks(row)
            
            for i, block in enumerate(mergedRow):
                block.pos[1] = i          
                
            self.addBuffer(mergedRow)
                    
        return self.updateBoard() # returns true if board updates
    
        
    def moveRight(self):
        """
        Moves all the blocks right
        """
        for i in range(self.size):
            row = [block for block in self.allBlocks if block.pos[0] == i]

            row.sort(key=lambda x: x.pos[1], reverse=True)
            
            for block in row:
                block.prevPos = block.pos.copy()
            
            mergedRow = self.mergeBlocks(row)
  
            for i, block in enumerate(mergedRow):
                block.pos[1] = self.size - (1+i) 
                
            self.addBuffer(mergedRow)
                    
        return self.updateBoard() # returns true if board updates
    
            
    def moveUp(self):
        """
        Moves all the blocks up
        """
        for i in range(self.size):
            col = [block for block in self.allBlocks if block.pos[1] == i]

            col.sort(key=lambda x: x.pos[0])
           
            for block in col:
                block.prevPos = block.pos.copy()                
            
            mergedCol = self.mergeBlocks(col)
  
            for i, block in enumerate(mergedCol):
                block.pos[0] = i
                
            self.addBuffer(mergedCol)
                    
        return self.updateBoard() # returns true if board updates
    
        
    def moveDown(self):
        """
        Moves all the blocks down
        """
        for i in range(self.size):
            col = [block for block in self.allBlocks if block.pos[1] == i]

            col.sort(key=lambda x: x.pos[0], reverse=True)
            
            for block in col:
                block.prevPos = block.pos.copy()
            
            mergedCol = self.mergeBlocks(col)
    
            for i, block in enumerate(mergedCol):
                block.pos[0] = self.size - (1+i)
                
            self.addBuffer(mergedCol)
                    
        return self.updateBoard() # returns true if board updates
  
    
    def mergeBlocks(self, blocks):
        """
        Merges the blocks of a row or column
        Returns the merged list
        """    
        mergedBlocks = []
        
        i = 0
        while True:
            try:
                if blocks[i].value == blocks[i+1].value:
                    #newBlock = Block(blocks[i].value*2, blocks[i].pos)
                    newBlock = copy.deepcopy(blocks[i])
                    newBlock.prevPos = blocks[i+1].pos.copy()
                    newBlock.doubleValue()
                    self.score += newBlock.value
                    mergedBlocks.append(newBlock)
                    blocks.pop(i+1)
                else:
                    newBlock = copy.deepcopy(blocks[i])
                    newBlock.updatePrev()
                    mergedBlocks.append(newBlock)              
            except: # this triggers on last iteration since i+1 out of range
                try: # add last block if its still in range
                    newBlock = copy.deepcopy(blocks[i])
                    newBlock.updatePrev()
                    mergedBlocks.append(newBlock)
                except:
                    break
                break 
            i += 1
            
        return mergedBlocks
                

    def printBoard(self):
        """
        Prints the board as an array
        """   
        board = np.zeros((self.size,self.size))
        
        for block in self.allBlocks:
            y, x = block.pos
            board[y][x] = block.value
            
        print(board)
        print("")
        
    
    def bestBlock(self):
        """
        Returns the highest value block
        """
        best = 0
        for block in self.allBlocks:
            if block.value > best:
                best = block.value
                
        return best

        
        
            
        
