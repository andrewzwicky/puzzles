from pathlib import Path
import itertools
from collections import Counter, namedtuple, defaultdict
from pprint import pprint
import re
from datetime import datetime
import numpy as np
import functools
from copy import copy, deepcopy
from enum import Enum, IntEnum

data = Path('input.txt').read_text().splitlines()
data = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"

data = data.strip('^').strip('$')

print()

results = ['']
depth = 0
index = 0

def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    return img[ymin:ymax+1, xmin:xmax+1]

for char in data:
    current = results
    for _ in range(depth):
        current = current[-1]

    if char == '(':
        current.append([''])
        depth += 1


    elif char == '|':
        current.append('')

    elif char == ')':
        depth -= 1

    else:
        try:
            current[-1] = current[-1] + char
        except TypeError:
            current.append('')
            current[-1] = current[-1] + char

grid_size = 2*len(data)+3
grid = np.zeros((grid_size,grid_size), dtype=int)
start = grid_size // 2
grid[start,start] = 1

# # = 0
# X = 1
# - = 2
# | = 3
# . = 4

printing_map = {
    0:'#',
    1:'X',
    2:'-',
    3:'|',
    4:'.'
}

#row, col
current = np.array([start,start])

directions = {
    'E':np.array([0,2]),
    'N':np.array([-2,0]),
    'W':np.array([0,-2]),
    'S':np.array([2,0]),}

door = {
    'E':np.array([0,1]),
    'N':np.array([-1,0]),
    'W':np.array([0,-1]),
    'S':np.array([1,0]),}



def recur_path(input_data, current_path, longest_path, current, grid):
    print()
    for segment in input_data:
        if type(segment) == str:
            for char in segment:
                r_d, c_d = current + door[char]
                current = current + directions[char]
                r,c = current
                grid[r,c] = 4
                grid[r_d,c_d] = 2 if char in 'NS' else 3
                current_path += char
                if len(current_path) > len(longest_path):
                    longest_path = current_path
            print()

        else:
            longest_path = recur_path(segment, current_path, longest_path, copy(current), grid)

    return longest_path

longest_path = recur_path(results, '', '', current, grid)

print(len(longest_path))