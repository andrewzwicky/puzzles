import sys

sys.argv.append('challenge_30_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        set1,set2 = list(map(set,[list(map(int,i.split(','))) for i in test.strip().split(';')]))
        inter = set1.intersection(set2)
        print(','.join(list(map(str,inter))))
