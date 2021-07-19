# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:17:04 2020

@author: iainr
"""
#ADD A PREV VALUE ATTRIBUTE!!!!!!!!!!!!!
class Block:
    def __init__(self, value, pos):
        
        self.value = value
        
        self.prevValue = value
    
        self.pos = pos
        
        self.prevPos = pos
            
        self.updateColour()
        
        self.merged = False
        
        
    def __eq__(self, o):
        return self.value == o.value and self.pos == o.pos
    
    
    def __hash__(self):
        return(hash(tuple(self.pos)))
    
    
    def doubleValue(self):
        self.prevValue = self.value
        self.value *= 2
        self.updateColour()
        self.merged = True
        
    
    def updatePrev(self):
        self.prevValue = self.value
        self.updateColour()
        self.merged = False
    
    
    def updateColour(self):
        colours = ({2: (150,150,150),
                    4: (120,120,120),
                    8: (255,236,139),
                    16: (255,140,0),
                    32: (238,44,44),
                    64: (192,255,62),
                    128: (84,139,84),
                    256: (65,105,225),
                    512: (39,64,139),
                    1024: (154,50,205),
                    2048: (104,34,139),
                    4096: (160,40,190),
                    8192: (30,150,150),
                    16384: (200,10,40),
                    32768: (100,145,200),
                    65536: (40,30,146),
                    131072: (153,56,175)})
        
        self.colour = colours[self.value]
        
        self.prevColour = colours[self.prevValue]
        
         
