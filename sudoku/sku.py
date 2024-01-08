import itertools
from pprint import pprint

DIGITS = list(range(1,10))

def print_nums(x):
    print(''.join([f'{n} ' for n in sorted(x)]).strip())

def count_to(target, start=0, used=set(), digits=DIGITS):
    for i, d in enumerate(digits):
        adjusted = start + d
        if adjusted > target:
            return
        elif adjusted == target:
            yield sorted(list(used.union({d})))
        else:
            yield from count_to(target, adjusted, used.union({d}), digits[i+1:])

def possibles(number):
    all_possibles = count_to(number)
    return sorted(all_possibles, key=lambda x: (len(x), min(x)))

def ranges(number):
    all_possibles = count_to(number)
    all_ranges = {len(x) for x in all_possibles}
    return list(sorted(all_ranges))
