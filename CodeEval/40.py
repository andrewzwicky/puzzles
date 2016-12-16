import sys
from collections import Counter
sys.argv.append('40_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        test = test.strip()
        count = Counter(test)
        self_desc = 1
        for indx, num in enumerate(test):
            if num != str(count[str(indx)]):
                self_desc = 0
        print(self_desc)
