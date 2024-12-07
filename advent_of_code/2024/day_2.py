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

DAY = 2




def split_into_nums(line):
    return tuple(map(int, line.split()))


def is_safe(num_list):
    n_arr = np.diff(num_list)
    # has zero
    if np.any(n_arr == 0):
        return False

    # all are same sign
    if np.all(n_arr > 0) if n_arr[0] > 0 else np.all(n_arr < 0):
        if np.max(np.absolute(n_arr)) > 3:
            return False
    else:
        return False

    return True


def iterate_is_safe(num_list):
    if is_safe(num_list):
        return True

    for i in range(len(num_list)):
        temp_list = num_list[:i] + num_list[i + 1 :]
        if is_safe(temp_list):
            return True

    return False


def part_1(data):
    nums = [split_into_nums(line) for line in data]

    result = [is_safe(num_arr) for num_arr in nums]

    return Counter(result)[True]


def part_2(data):
    nums = [split_into_nums(line) for line in data]

    result = [iterate_is_safe(num_arr) for num_arr in nums]

    return Counter(result)[True]


if __name__ == "__main__":
    _, true_data = get_problem_input(DAY)
    submit_answer(DAY, 1, part_1(true_data))
    submit_answer(DAY, 2, part_2(true_data))
