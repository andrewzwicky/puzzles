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

DAY = 1


def split_into_nums(line):
    return tuple(map(int, line.split()))


def part_1(data):
    num_pairs = [split_into_nums(l) for l in data]
    left, right = map(list, zip(*num_pairs))
    left.sort()
    right.sort()

    total = 0
    for l, r in zip(left, right):
        total += abs(l - r)

    return total


def part_2(data):
    num_pairs = [split_into_nums(l) for l in data]
    left, right = map(list, zip(*num_pairs))
    right_counter = Counter(right)

    left.sort()

    total = 0
    for l in left:
        total += l * right_counter[l]

    return total


if __name__ == "__main__":
    _, true_data = get_problem_input(DAY)
    submit_answer(DAY, 1, part_1(true_data))
    submit_answer(DAY, 2, part_2(true_data))
