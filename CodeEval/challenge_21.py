import sys


def challenge(input_string):
    return sum(map(int, input_string))


if __name__ == "__main__":
    with open(sys.argv[-1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))