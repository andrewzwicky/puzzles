from day_3 import part_1, part_2
from common import parse_problem_input

TEST_RAW = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
TEST_DATA = parse_problem_input(TEST_RAW)


def test_day_3_part_1():
    assert part_1(TEST_DATA) == 161


def test_day_3_part_2():
    assert part_2(TEST_DATA) == 48
