import sys


def challenge(input_string):
    equat = reversed(input_string.strip().split(' '))
    stack = []
    for char in equat:
        if char not in '+*/-':
            stack.append(char)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append(str(eval('{}{}{}'.format(a, char.replace('/', '//'), b))))
    return int(stack[0])


if __name__ == "__main__":
    with open(sys.argv[-1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))