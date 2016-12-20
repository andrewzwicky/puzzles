import sys
from collections import Counter


def challenge(input_string):
    count = Counter(input_string.strip())
    self_desc = 1
    for indx, num in enumerate(count):
        if num != str(count[str(indx)]):
            self_desc = 0
    return self_desc


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))
