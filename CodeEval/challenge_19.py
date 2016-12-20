import sys
from unittest import TestCase


def challenge(input_string):
    num, i, j = map(int, input_string.strip().split(','))
    num_string = '{:b}'.format(num)
    if num_string[::-1][i - 1] == num_string[::-1][j - 1]:
        return 'true'
    else:
        return 'false'


if __name__ == "__main__":
    with open(sys.argv[-1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))