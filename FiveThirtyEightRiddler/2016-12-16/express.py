# A geology museum in California has six different rocks
# sitting in a row on a shelf, with labels on the shelf 
# telling what type of rock each is. An earthquake hits 
# and the rocks all fall off the shelf. A janitor comes in
# and, wanting to clean the floor, puts the rocks back on
# the shelf in random order. The probability that the janitor 
# put all six rocks behind their correct labels is 1/6!, 
# or 1/720. But what are the chances that exactly five rocks
# are in the correct place, exactly four rocks are in the
# correct place, exactly three rocks are in the correct place, 
# exactly two rocks are in the correct place, exactly one
# rock is in the correct place, and none of the rocks 
# are in the correct place?

from collections import Counter
import itertools
ORDER = 'ABCDEF'

def count_same(input, correct):
    count=0
    for i,c in zip(input, correct):
        if i==c:
            count+=1
    return count


possibles = [''.join(new_order) for new_order in itertools.permutations(ORDER)]
total = len(possibles)
counts = Counter(count_same(input, ORDER) for input in possibles)
for num,pos, in counts.items():
    print("{} : {:2.2%}".format(num, pos/total))
