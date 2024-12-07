from common import get_problem_input, submit_answer, neighbors, parse_problem_input
import requests
from math import ceil, floor
from bs4 import BeautifulSoup
from collections import Counter, namedtuple
import re
from collections import defaultdict
from copy import copy, deepcopy
import itertools
from itertools import accumulate, zip_longest, pairwise, tee
from pprint import pprint
from functools import cache
import numpy as np
from enum import Enum, IntEnum, auto
from string import ascii_lowercase, ascii_uppercase
from dataclasses import dataclass, field
import operator
from typing import List, Tuple, Set, Dict
import functools
from operator import itemgetter

DAY = 4

FORWARD = "XMAS"
BACKWARD = "SAMX"

MAS_FORWARD = "MAS"
MAS_BACKWARD = "SAM"


def part_1(data):
    total = 0
    # horiz
    for line in data:
        total += line.count(FORWARD)
        total += line.count(BACKWARD)

    for line in ["".join(l) for l in zip(*data)]:
        total += line.count(FORWARD)
        total += line.count(BACKWARD)

    # rotate
    np_arr = np.array([[c for c in line] for line in data])

    for i in itertools.count():
        line = "".join(np_arr.diagonal(i))
        if len(line) < len(FORWARD):
            break
        total += line.count(FORWARD)
        total += line.count(BACKWARD)

    for i in itertools.count(-1, -1):
        line = "".join(np_arr.diagonal(i))
        if len(line) < len(FORWARD):
            break
        total += line.count(FORWARD)
        total += line.count(BACKWARD)

    for i in itertools.count():
        line = "".join(np.fliplr(np_arr).diagonal(i))
        if len(line) < len(FORWARD):
            break
        total += line.count(FORWARD)
        total += line.count(BACKWARD)

    for i in itertools.count(-1, -1):
        line = "".join(np.fliplr(np_arr).diagonal(i))
        if len(line) < len(FORWARD):
            break
        total += line.count(FORWARD)
        total += line.count(BACKWARD)

    return total


def part_2(data):
    mas_re_f = re.compile(MAS_FORWARD)
    mas_re_b = re.compile(MAS_BACKWARD)

    total = 0

    np_arr = np.array([[c for c in line] for line in data])

    d1_coords = []
    d2_coords = []

    for i in itertools.count():
        line = "".join(np_arr.diagonal(i))
        if len(line) < len(MAS_FORWARD):
            break
        for m in list(mas_re_f.finditer(line)):
            idx = m.span()[0] + 1
            d1_coords.append(complex(idx, i + idx))
        for m in list(mas_re_b.finditer(line)):
            idx = m.span()[0] + 1
            d1_coords.append(complex(idx, i + idx))

    for i in itertools.count(-1, -1):
        line = "".join(np_arr.diagonal(i))
        if len(line) < len(MAS_FORWARD):
            break
        for m in list(mas_re_f.finditer(line)):
            idx = m.span()[0] + 1
            d1_coords.append(complex(idx + abs(i), idx))
        for m in list(mas_re_b.finditer(line)):
            idx = m.span()[0] + 1
            d1_coords.append(complex(idx + abs(i), idx))

    _, max_x = np_arr.shape

    for i in itertools.count():
        line = "".join(np.fliplr(np_arr).diagonal(i))
        if len(line) < len(MAS_FORWARD):
            break
        for m in list(mas_re_f.finditer(line)):
            idx = m.span()[0] + 1
            d2_coords.append(complex(idx, max_x - 1 - (i + idx)))
        for m in list(mas_re_b.finditer(line)):
            idx = m.span()[0] + 1
            d2_coords.append(complex(idx, max_x - 1 - (i + idx)))

    for i in itertools.count(-1, -1):
        line = "".join(np.fliplr(np_arr).diagonal(i))
        if len(line) < len(MAS_FORWARD):
            break
        for m in list(mas_re_f.finditer(line)):
            idx = m.span()[0] + 1
            d2_coords.append(complex(idx + abs(i), max_x - 1 - idx))
        for m in list(mas_re_b.finditer(line)):
            idx = m.span()[0] + 1
            d2_coords.append(complex(idx + abs(i), max_x - 1 - idx))

    total = len(set.intersection(set(d1_coords), set(d2_coords)))

    return total


if __name__ == "__main__":
    _, true_data = get_problem_input(DAY)
    submit_answer(DAY, 1, part_1(true_data))
    submit_answer(DAY, 2, part_2(true_data))
