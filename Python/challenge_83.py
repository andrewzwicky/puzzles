import sys

sys.argv.append('challenge_83_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        print(*test.strip().split(' ')[::-1])