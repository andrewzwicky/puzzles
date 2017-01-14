"""
You and I stumble across a 100-sided die in our local game shop.
We know we need to have this die — there is no question about it
— but we’re not quite sure what to do with it. So we devise a
simple game: We keep rolling our new purchase until one roll shows
a number smaller than the one before. Suppose I give you a dollar
every time you roll. How much money do you expect to win?
"""

import random
from collections import Counter
from matplotlib import pyplot as plt
import itertools


def simulate_rolls(dice_size):
    last_roll = random.randint(1,dice_size)
    number_of_rolls = 1

    while True:
        this_roll = random.randint(1,dice_size)
        number_of_rolls += 1
        if this_roll < last_roll:
            break
        else:
            last_roll = this_roll

    return number_of_rolls

#print(Counter(simulate_rolls(100) for _ in range(1000000)))
#res = Counter({2: 494883, 3: 333562, 4: 127529, 5: 34764, 6: 7581, 7: 1426, 8: 213, 9: 38, 10: 4})
plt.plot([2,3,4,5,6,7,8,9,10],list(itertools.accumulate([494883, 333562,127529,34764,7581,1426,213,38,4])))
plt.show()