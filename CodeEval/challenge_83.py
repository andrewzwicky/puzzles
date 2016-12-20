import sys
from unittest import TestCase


def challenge(input_string):
    pass


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))
