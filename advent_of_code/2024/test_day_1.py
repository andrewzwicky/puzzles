from day_1 import part_1, part_2
from common import parse_problem_input

TEST_RAW = """3   4
4   3
2   5
1   3
3   9
3   3"""
TEST_DATA = parse_problem_input(TEST_RAW)


def test_day_1_part_1():
    assert part_1(TEST_DATA) == 11


def test_day_1_part_2():
    assert part_2(TEST_DATA) == 31
