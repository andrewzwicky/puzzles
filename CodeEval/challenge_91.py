import sys


def challenge(input_string):
    test2 = list(map(float, input_string.strip().split(' ')))
    return ' '.join('{:-.3f}'.format(n) for n in sorted(test2))


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))