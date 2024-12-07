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

DAY = 5


def is_correct(rules, sequence):
    for i, curr in enumerate(sequence):
        checks = [x in rules[curr] for x in sequence[i + 1 :]]
        if any(checks):
            return False, None
    return True, sequence[len(sequence) // 2]


def reorder(rules, sequence):
    new_seq = list(sequence)
    for curr in sequence:
        new_seq[Counter([s in rules[curr] for s in sequence])[True]] = curr
    return new_seq


def part_1(data):
    rules = defaultdict(list)
    sequences = []
    in_seq = False
    for line in data:
        if not line:
            in_seq = True
            continue

        if in_seq:
            sequences.append(tuple(map(int, line.split(","))))
        else:
            a, b = map(int, line.split("|"))
            rules[b].append(a)

    total = 0
    for s in sequences:
        corr, num = is_correct(rules, s)
        if corr:
            total += num

    return total


def part_2(data):
    rules = defaultdict(list)
    sequences = []
    in_seq = False
    for line in data:
        if not line:
            in_seq = True
            continue

        if in_seq:
            sequences.append(tuple(map(int, line.split(","))))
        else:
            a, b = map(int, line.split("|"))
            rules[b].append(a)

    total = 0
    for s in sequences:
        corr, _ = is_correct(rules, s)
        if not corr:
            new_seq = reorder(rules, s)
            total += new_seq[len(new_seq) // 2]

    return total


if __name__ == "__main__":
    _, true_data = get_problem_input(DAY)
    submit_answer(DAY, 1, part_1(true_data))
    submit_answer(DAY, 2, part_2(true_data))
