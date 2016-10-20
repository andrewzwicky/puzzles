import sys

sys.argv.append('challenge_XX_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases: