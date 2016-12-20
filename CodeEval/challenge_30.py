import sys


def challenge(input_string):
    set1, set2 = list(map(set, [list(map(int, i.split(','))) for i in input_string.strip().split(';')]))
    inter = set1.intersection(set2)
    return ','.join(list(map(str, inter)))


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))