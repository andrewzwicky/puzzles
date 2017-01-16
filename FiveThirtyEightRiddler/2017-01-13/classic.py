"""
You and I stumble across a 100-sided die in our local game shop.
We know we need to have this die — there is no question about it
— but we’re not quite sure what to do with it. So we devise a
simple game: We keep rolling our new purchase until one roll shows
a number smaller than the one before. Suppose I give you a dollar
every time you roll. How much money do you expect to win?

Extra credit:
What happens to the amount of money as the number of sides increases?
"""

import random
from collections import Counter
from matplotlib import pyplot as plt
import multiprocessing
import itertools

TOTAL = 10000000


def simulate_rolls(dice_size):
    last_roll = random.randint(1, dice_size)
    number_of_rolls = 1

    while True:
        this_roll = random.randint(1, dice_size)
        number_of_rolls += 1
        if this_roll < last_roll:
            break
        else:
            last_roll = this_roll

    return number_of_rolls


pool = multiprocessing.Pool()

for dice in [10, 100, 200, 500, 1000]:
    res = Counter(pool.map(simulate_rolls, [dice for _ in range(TOTAL)]))

    plt.plot(list(res.keys()),
             list(count / TOTAL for count in itertools.accumulate(res.values())),
             marker=".",
             markersize=10,
             label=dice)

plt.legend()
plt.show()
