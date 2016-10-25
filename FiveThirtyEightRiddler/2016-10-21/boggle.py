import numpy as np

def word_gen():
    with open('../enable1.txt','r') as word_list:
        for line in word_list:
            yield line.strip()

SIZE = 4

def solve(input_grid):
    grid = input_grid.split()
    possibles = set(input_grid)
    possibles.remove(' ')
    
    boggle_alpha = [word for word in word_gen() if len(word) > 3 and set(word) <= possibles]
    
    print('done')
    
def neighbors(x,y):
    # range has to be +1 because it is not inclusive
    for nx in range(max(0,x-1),min(x+2,SIZE)):
        for ny in range(max(0,y-1),min(y+2,SIZE)):
            yield (nx,ny)
    

solve("abcd reft regt uvfo")
