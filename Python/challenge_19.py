import sys

sys.argv.append('challenge_19_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        num, i, j = map(int,test.strip().split(','))
        num_string = '{:b}'.format(num)
        if num_string[::-1][i-1] == num_string[::-1][j-1]:
            print('true')
        else:
            print('false')
        
        
