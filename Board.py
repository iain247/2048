# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:12:43 2020

@author: iainr
"""

import pygame, random, collections, copy, time, threading, math
from Block import Block

class Board:
    def __init__(self, length=500, size=4):
        
        self.score = 0
        self.highScore = 0
        self.status = True # game is ongoing
        
        self.frameRate = 8
        
        self.allBlocks = []
        self.buffer = []
        
        self.length = length
        self.topSize = length//5
        self.size = size
        self.scaling = length/500
             
        #some required geometric specificaitons
        self.thickness = 8*self.scaling # line thickness
        self.boxSize = (self.length - 5*self.thickness)/size # box size
        
        #some colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.lightGrey = (210,210,210)
        self.darkGrey = (100,100,100)
        
        pygame.init()
        self.screen = pygame.display.set_mode([self.length, self.length+self.topSize])
        
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
        resets board as well as buffer, list of blocks and score
        """       
        self.status = True
        self.allBlocks = []
        self.buffer = []
        
        self.score = 0   
            
        self.drawGame()
        self.createNewBlock()
        self.createNewBlock()
            
        
    def drawGame(self):
        """
        Draws an empty board
        """        
        self.screen.fill(self.white)           
        rect = pygame.Rect(0, self.topSize, self.length, self.length)
        pygame.draw.rect(self.screen, self.lightGrey, rect)
        
        self.drawLines()
        self.updateScore()
        self.updateHighScore(self.highScore)
        
        font = pygame.font.SysFont('8-Bit-Madness', math.floor(self.scaling*40))
        message = "New Game"
        txt = font.render(message, True, self.black)
        size = font.size(message)   
        
        drawX = 3*self.length/4 - size[0]/2
        drawY = self.topSize/2 - size[1]/2
        
        self.resetButton = pygame.Rect(drawX, drawY, size[0], size[1])
        pygame.draw.rect(self.screen, self.white, self.resetButton)

        self.screen.blit(txt, (drawX,drawY))
        
    
    def updateScore(self):
        """
        Updates the score shown in the top left
        """              
        font = pygame.font.SysFont('8-Bit-Madness', math.floor(self.scaling*40))
        message = "Score: " + str(self.score)
        txt = font.render(message, True, self.black)
        size = font.size(message)   
        
        drawX = self.length/4 - size[0]/2
        drawY = self.topSize/4 - size[1]/2
        
        border = 5*self.scaling
        
        rect = pygame.Rect(drawX-border, drawY-border,
                           size[0]+2*border, size[1]+2*border)
        pygame.draw.rect(self.screen, self.white, rect)

        self.screen.blit(txt, (drawX,drawY))
        
        if self.score >= self.highScore:
            self.updateHighScore(self.score)
        
    
    def updateHighScore(self, score):
        """
        Updates the highscore shown in the top left
        """       
        self.highScore = score
        
        font = pygame.font.SysFont('8-Bit-Madness', math.floor(self.scaling*40))
        message = "Highscore: " + str(self.highScore)
        txt = font.render(message, True, self.black)
        size = font.size(message)   
        
        drawX = self.length/4 - size[0]/2
        drawY = 3*self.topSize/4 - size[1]/2
        
        border = 5*self.scaling
        
        rect = pygame.Rect(drawX-border, drawY-border,
                           size[0]+2*border, size[1]+2*border)
        pygame.draw.rect(self.screen, self.white, rect)

        self.screen.blit(txt, (drawX,drawY))
        
        pygame.display.update()
                
                
    def getCoord(self, pos):
        """
        Returns the left and top coordinate of a specific cell
        """                   
        top = self.topSize + self.thickness + pos[0]*(self.boxSize + self.thickness)
        left = self.thickness + pos[1]*(self.boxSize + self.thickness)
        
        return left, top
        
        
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
                block.updatePrev()
            
            return False
        
        self.allBlocks = copy.deepcopy(self.buffer)
            
        self.buffer = []
        
        self.updateScore()
              
        return True
               
        
    def drawBlock(self, left, top, colour, value, update=True):
        """
        Adds a block to the board based on its left and top coordinates, its
        colour, and its value
        If update=False, the screen is not updated
        """       
        width = 4
        
        outline = pygame.Rect(left-width, top-width, 
                              self.boxSize+2*width, self.boxSize+2*width)
        pygame.draw.rect(self.screen, self.darkGrey, outline)
        
        rect = pygame.Rect(left, top, self.boxSize, self.boxSize)
        pygame.draw.rect(self.screen, colour, rect)
        
        font = pygame.font.SysFont('8-Bit-Madness', math.floor(self.scaling*45))
        num = str(value)
        txt = font.render(num, True, self.black)
        size = font.size(num)   

        drawX = left + self.boxSize/2 - size[0]/2
        drawY = top + self.boxSize/2 - size[1]/2

        self.screen.blit(txt, (drawX,drawY))
        
        if update:        
            pygame.display.update()
        
        
    def addBuffer(self, blocks):
        """
        Adds blocks to the list of blocks on the board
        """
        for x in blocks:
            self.buffer.append(x)
                
        
    def createNewBlock(self):
        """
        Creates a new block of either 2 or 4 at a random position
        """                                    
        startNum = [2,2,2,2,2,2,2,2,2,4] # 10% chance of a 4

        value = random.choice(startNum)
        
        while True:
            pos = [random.randint(0,3), random.randint(0,3)]
            if self.cellStatus(pos):
                break
                
        newBlock = Block(value, pos)
        
        left, top = self.getCoord(pos)       
        self.drawBlock(left, top, newBlock.colour, newBlock.value)
        
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
        self.gameOver()

                   
    def gameOver(self):
        """
        Shows 'game over' on the screen
        """       
        font = pygame.font.SysFont('8-Bit-Madness', math.floor(self.scaling*80))
        message = "Game Over!"
        txt = font.render(message, True, self.black)
        size = font.size(message)   
        
        drawX = self.length/2 - size[0]/2
        drawY = self.topSize + self.length/2 - size[1]/2
        
        time.sleep(0.5)

        self.screen.blit(txt, (drawX,drawY))
        
        pygame.display.update()
        
        time.sleep(1)
                
           
    def moveLeft(self, test=False):
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
                    
        status = self.updateBoard() # returns true if board updates
            
        self.move("left")

        return status
    
        
    def moveRight(self):
        """
        Moves all blocks to the right
        New blocks are stored in the buffer and then updated
        Returns true if a new move is possible
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
                    
        status = self.updateBoard() # returns true if board updates
        
        self.move("right")
            
        return status
    
            
    def moveUp(self):
        """
        Moves all blocks up
        New blocks are stored in the buffer and then updated
        Returns true if a new move is possible
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
                    
        status = self.updateBoard() # returns true if board updates
        
        self.move("up")
            
        return status
    
        
    def moveDown(self):
        """
        Moves all blocks down
        New blocks are stored in the buffer and then updated
        Returns true if a new move is possible
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
                    
        status = self.updateBoard() # returns true if board updates
        
        self.move("down")
                   
        return status
    
    
    def mergeBlocks(self, blocks):
        """
        Takes an row or column of blocks, adjacent blocks of the same value 
        are merged
        A new merged list is returned
        """     
        # not the cleanest code :/        
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
  
    
    def move(self, direction):
        """
        Shows the blocks moving from their previous to new position
        """      
        direction = direction
               
        for i in range(1,self.frameRate):
            
            frame = i/self.frameRate
            
            for block in self.allBlocks:
                
                if block.pos == block.prevPos:
                    continue
                
                self.drawFrame(block, direction, frame)
                
            self.drawLines()                  
                
            time.sleep(0.15/self.frameRate)
                
            pygame.display.update()
            
        # last frame shows current value and colour    
                
        for block in self.allBlocks:
                       
            self.drawFrame(block, direction, 1, True)

        self.drawLines()              
                
        pygame.display.update()  
        
        
    def drawFrame(self, block, direction, frame, final = False):
        """
        Draws a frame of the block moving from old to new position
        """        
        direction = direction
        
        startLeft, startTop = self.getCoord(block.prevPos)       
        endLeft, endTop = self.getCoord(block.pos)
        
        leftDiff = endLeft - startLeft
        topDiff = endTop - startTop
                     
        left = startLeft + frame * leftDiff
        top = startTop + frame * topDiff
        
        dLeft = abs(startLeft-left)
        dTop = abs(startTop-top)
        
        if direction == "left":
            rect = pygame.Rect(left+self.boxSize, top, dLeft, self.boxSize)
        elif direction == "right":
            rect = pygame.Rect(startLeft, top, dLeft, self.boxSize)
        elif direction == "up":
            rect = pygame.Rect(left, top+self.boxSize, self.boxSize, dTop)
        elif direction == "down":
            rect = pygame.Rect(left, startTop, self.boxSize, dTop)
        pygame.draw.rect(self.screen, self.lightGrey, rect)
        
        if final:   
            
            if block.merged:
                # new thread for emphasizing so you don't have to wait for
                # emphasizing animation before updating next block.
                # probably not necessary
                x = threading.Thread(target=self.emphasize, args=(block,))
                x.start()
            else: 
                self.drawBlock(left, top, block.colour, block.value, False)
                
        else:
            self.drawBlock(left, top, block.prevColour, block.prevValue, False)
               
           
    def drawLines(self):
        """
        Draws the dark grey horizontal and vertical lines of the game
        """
        left = 0
        top = 0
        
        for i in range(self.size+1):
            left = i * (self.boxSize+self.thickness)
            top = self.topSize + i * (self.boxSize+self.thickness)
            
            rectV = pygame.Rect(left, self.topSize, self.thickness, self.length)
            rectH = pygame.Rect(0, top, self.length, self.thickness)
            
            pygame.draw.rect(self.screen, self.darkGrey, rectV)
            pygame.draw.rect(self.screen, self.darkGrey, rectH)
        
        
    def emphasize(self, block):
        """
        Emphasizes blocks that merge together
        """
        left, top = self.getCoord(block.pos)
        
        rect = pygame.Rect(left, top, self.boxSize, self.boxSize)
        pygame.draw.rect(self.screen, 
                         block.colour, rect)
       
        font = pygame.font.SysFont('8-Bit-Madness', math.floor(self.scaling*64))
        num = str(block.value)
        txt = font.render(num, True, self.black)
        size = font.size(num)   

        drawX = left + self.boxSize/2 - size[0]/2
        drawY = top + self.boxSize/2 - size[1]/2

        self.screen.blit(txt, (drawX,drawY))
        
        time.sleep(0.15)
        
        self.drawBlock(left, top, block.colour, block.value)
        
        pygame.display.update()
        
        