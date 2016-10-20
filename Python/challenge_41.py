import sys
from collections import Counter

sys.argv.append('challenge_41_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        array = [int(i) for i in test.strip().split(';')[1].split(',')]
        num, count = Counter(array).most_common(1)[0]
        print(num)
