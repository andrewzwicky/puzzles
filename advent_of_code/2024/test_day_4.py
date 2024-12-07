from day_4 import part_1, part_2
from common import parse_problem_input

TEST_RAW = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
TEST_DATA = parse_problem_input(TEST_RAW)


def test_day_4_part_1():
    assert part_1(TEST_DATA) == 18


def test_day_4_part_2():
    assert part_2(TEST_DATA) == 9
