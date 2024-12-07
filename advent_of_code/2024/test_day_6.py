from day_6 import part_1, part_2, would_loop_blocked_here, convert_chars_to_arr, D
from common import parse_problem_input
import pytest
import numpy as np

TEST_RAW = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
TEST_DATA = parse_problem_input(TEST_RAW)


def test_day_6_part_1():
    assert part_1(TEST_DATA) == 41

inputs = [
    (TEST_DATA, 1, 8, D.S, False, None),
    (TEST_DATA, 4, 8, D.S, False, None),
    (TEST_DATA, 6, 4, D.N, False, None),
    (TEST_DATA, 6, 4, D.W, True, np.array([6,3])),
    (TEST_DATA, 6, 6, D.N, False, None),
    (TEST_DATA, 6, 6, D.S, True, np.array([7,6])),
    (TEST_DATA, 7, 6, D.E, True, np.array([7,7])),
    (TEST_DATA, 7, 6, D.N, False, None),
    (TEST_DATA, 8, 1, D.W, False, None),
    (TEST_DATA, 8, 2, D.E, False, None),
    (TEST_DATA, 8, 2, D.S, False, None),
    (TEST_DATA, 8, 2, D.W, True, np.array([8,1])),
    (TEST_DATA, 8, 4, D.N, False, None),
    (TEST_DATA, 8, 4, D.W, True, np.array([8,3])),
    (TEST_DATA, 8, 7, D.N, False, None),
    (TEST_DATA, 8, 7, D.S, True, np.array([9,7])),
    (TEST_DATA, 9, 9, D.E, False, None),
    (TEST_DATA, 9, 9, D.N, False, None),
    (TEST_DATA, 9, 9, D.S, False, None),
    (TEST_DATA, 9, 9, D.W, False, None),
]

@pytest.mark.parametrize("data, row, col, direct, result, exp_blocker", inputs)
def test_day_6_would_loop(data, row, col, direct, result, exp_blocker):
    arr, _, _ = convert_chars_to_arr(data)
    actual, blocker = would_loop_blocked_here(arr, row, col, direct)
    assert actual == result
    assert np.array_equal(blocker, exp_blocker)

def test_day_6_part_2():
    assert part_2(TEST_DATA) == 6
