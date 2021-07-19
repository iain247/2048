# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:29:47 2020

@author: iainr
"""

#x = [1,2,2,2,4,5,6,6,6,6,7]
x = [1,1]

def merge(x,reverse = False):
    
    
    if len(x) <= 1:
        return x
    
    # reverse the list (for right and down merging)
    if reverse:
        x.reverse()
        
    buffer = []

    i = 0
    while True:

        try:
            if x[i] == x[i+1]:
                buffer.append(x[i]*2)
                i += 2
            else:
                buffer.append(x[i])
                i += 1
        except:
            try:
                buffer.append(x[i])
            except:
                break
            break

        
    # # initialise empty list of merged blocks
    # merged = []
            
    # # loop for comparing values of consecutive blocks
    # i = 0 # dont consider first iteration
    # while i < len(x)-1:
    #     print(i)
    #     currBlock = x[i]
    #     nextBlock = x[i+1]
    #     if currBlock == nextBlock: # compare consecutive block values
    #         currBlock *= 2
    #         if i == len(x) - 3:
    #             merged.append(currBlock)
    #             merged.append(x[i+2])
    #             break        
    #         i += 2
            
    #     elif i == len(x) - 2: # catch for if no pair on last 2 blocks
    #         merged.append(currBlock)
    #         merged.append(nextBlock)
    #         break
    #     else:
    #         i += 1
            
    #     merged.append(currBlock)
    
    # # reverse back to normal for right and down merging
    if reverse:
        buffer.reverse()
        
    return buffer


print(merge(x))
print(merge(x,True))