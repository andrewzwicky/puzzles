import sys

if __name__ == "__main__":
    with open(sys.argv[-1], 'r') as test_cases:
        print(sum(map(int, test_cases)))