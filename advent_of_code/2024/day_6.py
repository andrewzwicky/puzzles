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
from enum import Enum, IntEnum, auto, IntFlag
from string import ascii_lowercase, ascii_uppercase
from dataclasses import dataclass, field
import operator
from typing import List, Tuple, Set, Dict
import functools
from operator import itemgetter

DAY = 6


class D(IntFlag):
    _ = auto()
    N = auto()
    E = auto()
    S = auto()
    W = auto()
    X = auto()
    L = auto()


def convert_chars_to_arr(data):
    arr_in = np.array([list(x) for x in data])
    row, col = tuple(map(int, np.where(arr_in == "^")))

    arr = np.zeros(arr_in.shape, dtype=D)

    arr[row, col] = D.N
    arr[np.where(arr_in != "#")] = D._
    arr[np.where(arr_in == "#")] = D.X
    return arr, row, col


def part_1(data):
    arr, row, col = convert_chars_to_arr(data)

    direct = D.N

    while True:
        if direct == D.N:
            s2 = np.s_[row::-1, col]
            s3 = np.s_[:, row::-1, col]
        elif direct == D.E:
            s2 = np.s_[row, col:]
            s3 = np.s_[:, row, col:]
        elif direct == D.S:
            s2 = np.s_[row:, col]
            s3 = np.s_[:, row:, col]
        else:
            s2 = np.s_[row, col::-1]
            s3 = np.s_[:, row, col::-1]

        indices = np.indices(arr.shape)[s3]
        ray = arr[s2]
        isin = np.invert(ray == D.X)
        # set everythin after first false to False
        if not np.all(isin):
            isin[np.argmax(isin == 0) :] = False

        # dist = len(path)
        arr[*indices.T[isin].T] &= ~D._
        arr[*indices.T[isin].T] |= direct
        row, col = indices.T[isin][-1].T

        if np.all(isin):
            break

        if direct == D.N:
            direct = D.E
        elif direct == D.E:
            direct = D.S
        elif direct == D.S:
            direct = D.W
        else:
            direct = D.N

    return (
        len(arr.flatten())
        - Counter([(D.X in x) or (x == D._) for x in arr.flatten()])[True]
    )


def would_loop_blocked_here(arr, row, col, direct):
    # start = np.array([row, col])
    pivots = set()

    if direct == D.N:
        temp_block = np.array([row - 1, col])
    elif direct == D.E:
        temp_block = np.array([row, col + 1])
    elif direct == D.S:
        temp_block = np.array([row + 1, col])
    else:
        temp_block = np.array([row, col - 1])

    try:
        if D.X in arr[*temp_block]:
            return (False, None)
    except IndexError:
        return (False, None)

    original_temp = arr[*temp_block]
    arr[*temp_block] = D.X

    pivots.add((direct, row, col))

    # loop check only needs 4 segments
    while True:
        if direct == D.N:
            direct = D.E
        elif direct == D.E:
            direct = D.S
        elif direct == D.S:
            direct = D.W
        else:
            direct = D.N

        if direct == D.N:
            s2 = np.s_[row::-1, col]
            s3 = np.s_[:, row::-1, col]
        elif direct == D.E:
            s2 = np.s_[row, col:]
            s3 = np.s_[:, row, col:]
        elif direct == D.S:
            s2 = np.s_[row:, col]
            s3 = np.s_[:, row:, col]
        else:
            s2 = np.s_[row, col::-1]
            s3 = np.s_[:, row, col::-1]

        indices = np.indices(arr.shape)[s3]
        ray = arr[s2]
        isin = np.invert(ray == D.X)
        # set everythin after first false to False
        if not np.all(isin):
            isin[np.argmax(isin == 0) :] = False
        else:
            arr[*temp_block] = original_temp
            return (False, None)

        row, col = indices.T[isin][-1].T
        pivot = (direct, row, col)
        if pivot in pivots:
            break
        pivots.add(pivot)

    arr[*temp_block] = original_temp
    return (True, temp_block)


def part_2(data):
    arr, row, col = convert_chars_to_arr(data)

    direct = D.N

    while True:
        if direct == D.N:
            s2 = np.s_[row::-1, col]
            s3 = np.s_[:, row::-1, col]
        elif direct == D.E:
            s2 = np.s_[row, col:]
            s3 = np.s_[:, row, col:]
        elif direct == D.S:
            s2 = np.s_[row:, col]
            s3 = np.s_[:, row:, col]
        else:
            s2 = np.s_[row, col::-1]
            s3 = np.s_[:, row, col::-1]

        indices = np.indices(arr.shape)[s3]
        ray = arr[s2]
        isin = np.invert(ray == D.X)
        # set everythin after first false to False
        if not np.all(isin):
            isin[np.argmax(isin == 0) :] = False

        for _r, _c in indices.T[isin]:
            p, l = would_loop_blocked_here(arr, _r, _c, direct)
            if p:
                arr[*l] |= D.L

        arr[*indices.T[isin].T] &= ~D._
        arr[*indices.T[isin].T] |= direct
        row, col = indices.T[isin][-1].T

        if np.all(isin):
            break

        if direct == D.N:
            direct = D.E
        elif direct == D.E:
            direct = D.S
        elif direct == D.S:
            direct = D.W
        else:
            direct = D.N

    return Counter([(D.L in x) for x in arr.flatten()])[True]


if __name__ == "__main__":
    _, true_data = get_problem_input(DAY)
    submit_answer(DAY, 1, part_1(true_data))
    submit_answer(DAY, 2, part_2(true_data))
