from itertools import product
from collections import Counter
from copy import copy
from time import sleep

class LifeGrid(object):
    
    def __init__(self, input):
        self.tf_map = {False:'.', True:'#',
                       '.':False, '#':True}
        self.grid = [[self.tf_map[i] for i in row] for row in input.split('\n')]
        if len(set(map(len,self.grid))) != 1:
            raise ValueError
        self.height = len(self.grid)
        self.width = len(self.grid[0])
            
            
    def __str__(self):
        result='''\n'''
        for row in self.grid:
            for spot in row:
                result += self.tf_map[spot]
            result += '\n'
        return result

    def __repr__(self):
        return self.__str__()

    def find_neighbors(self, x, y):
        if x<0 or x>self.width or y<0 or y>self.height:
            raise ValueError
        coords = list(product(range(x-1,x+2),range(y-1,y+2)))
        coords.remove((x,y))
        coords_wrap = map(lambda coord: (coord[0] % self.width, coord[1] % self.height), coords)
        
        return Counter(self.grid[x][y] for x,y in coords_wrap)

    def update_grid(self):
        new_grid = copy(self.grid)
        for x,y in product(range(0,self.width),range(0,self.height)):
            neighbors = self.find_neighbors(x,y)
            if self.grid[x][y]:
                if neighbors[True] < 2 or neighbors[True] > 3:
                    new_grid[x][y]=False
            else:
                if neighbors[True] == 3:
                    new_grid[x][y]=True
        self.grid = new_grid

if __name__ == '__main__':
    test = LifeGrid('''..........
..........
..#.......
...#......
.###......
..........
..........
..........
..........
..........
..........''')

    while True:
        test.update_grid()
        print(test)
        sleep(0.1)
        print('\n'*100)
