import sys


def challenge(input_string):
    return ' '.join(reversed(input_string.strip().split(' ')))

if __name__ == "__main__":
    with open(sys.argv[-1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))