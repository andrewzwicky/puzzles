import sys

sys.argv.append('challenge_7_input.txt')

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        equat = reversed(test.strip().split(' '))
        stack = []
        for char in equat:
            if char not in '+*/-':
                stack.append(char)
            else:
                a=stack.pop()
                b=stack.pop()
                stack.append(str(eval('{}{}{}'.format(a,char.replace('/','//'),b))))
        print(stack[0])
