import sys
from unittest import TestCase
from collections import Counter


def challenge(input_string):
    array = [int(i) for i in input_string.strip().split(';')[1].split(',')]
    num, count = Counter(array).most_common(1)[0]
    return num


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))