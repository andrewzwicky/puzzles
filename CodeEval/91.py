import sys

sys.argv.append('91_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        test2 = list(map(float,test.strip().split(' ')))
        for n in sorted(test2):
            print('{:-.3f}'.format(n), end=' ')
        print('')
