import itertools
import re
from copy import copy
from enum import IntEnum
from pathlib import Path

import numpy as np


class Spaces(IntEnum):
    Empty = 0
    Clay = 1
    Filled = 3
    Falling = 4


data = Path('input.txt').read_text().splitlines()
data = Path('test.txt').read_text().splitlines()

coordinates = []
for line in data:
    nums = list(map(int, re.findall(r'\d+', line)))
    if line[0] == 'x':
        x, *y = nums
        x = [x]
    else:
        y, *x = nums
        y = [y]

    coordinates.append((x, y))

all_x, all_y = [list(itertools.chain.from_iterable(axis)) for axis in list(zip(*coordinates))]

min_x = min(all_x)
max_x = max(all_x)

min_y = min(all_y)
max_y = max(all_y)

water = np.zeros((max_y + 1, (max_x + 1) - (min_x - 1)), dtype=int)

for x, y in coordinates:
    if len(x) > 1:
        water[y[0], x[0] - min_x:x[1] - min_x] = Spaces.Clay
    else:
        water[y[0]:y[1] + 1, x[0] - min_x] = Spaces.Clay

fill_points = [(500 - min_x, 0)]

for _ in range(20):
    for source_x, source_y in copy(fill_points):
        stream = water[source_y:, source_x]
        y_stop = np.where(np.logical_or(stream == Spaces.Clay, stream == Spaces.Filled))[0]
        if len(y_stop):
            y_stop = y_stop[0]
        else:
            if np.all(stream == Spaces.Empty):  # bottom of track
                y_stop = len(stream)
            else:
                y_stop = 0
        y_stop += source_y

        water[source_y:y_stop, source_x] = Spaces.Falling
        fill_points.remove((source_x, source_y))
        fill_points.append((source_x, y_stop))

        # fill
        overflow = [False, False]
        left = water[y_stop - 1, :source_x][::-1]
        fill_left = np.where(np.logical_and(left != Spaces.Empty, left != Spaces.Falling))[0]
        if len(fill_left):
            left_indx = source_x - fill_left[0]
        else:
            left_indx = source_x - len(left)

        right = water[y_stop - 1, source_x:]
        fill_right = np.where(np.logical_and(right != Spaces.Empty, right != Spaces.Falling))[0]
        if len(fill_right):
            right_indx = source_x + fill_right[0]
        else:
            right_indx = source_x + len(right)

        supports = water[y_stop, left_indx:right_indx] == Spaces.Empty

        if any(overflow):
            pass

        else:
            water[y_stop - 1, left_indx:right_indx] = Spaces.Filled

            fill_points.remove((source_x, y_stop))
            fill_points.append((source_x, y_stop - 1))

        print()

print(water)
