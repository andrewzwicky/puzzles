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

DAY = 3


def part_1(data):
    mul_re = re.compile(r"mul\((\d+),(\d+)\)")
    result = 0
    for line in data:
        x = mul_re.findall(line)
        for a, b in x:
            result += int(a) * int(b)
    return result


def part_2(data):
    mul_re = re.compile(r"(mul\((\d+),(\d+)\))|(do)\(\)|(don't)\(\)")
    result = 0
    do = True
    for line in data:
        x = mul_re.findall(line)
        for _, a, b, is_do, is_dont in x:
            if is_dont:
                do = False
            elif is_do:
                do = True
            elif do:
                result += int(a) * int(b)
    return result


if __name__ == "__main__":
    _, true_data = get_problem_input(DAY)
    submit_answer(DAY, 1, part_1(true_data))
    submit_answer(DAY, 2, part_2(true_data))
