from day_2 import part_1, part_2
from common import parse_problem_input

TEST_RAW = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
TEST_DATA = parse_problem_input(TEST_RAW)


def test_day_2_part_1():
    assert part_1(TEST_DATA) == 2


def test_day_2_part_2():
    assert part_2(TEST_DATA) == 4
