"""
You and I find ourselves indoors one rainy afternoon, with nothing but some loose change in the couch cushions to
entertain us. We decide that we’ll take turns flipping a coin, and that the winner will be whoever flips 10 heads
first. The winner gets to keep all the change in the couch! Predictably, an enormous argument erupts: We both want
to be the one to go first.

What is the first flipper’s advantage? In other words, what percentage of the time does the first flipper win this game?
"""
from math import factorial
import itertools
from matplotlib import pyplot as plt
import random
from multiprocessing import Pool
from collections import Counter


def binomial(odds, successes, trials):
    a = (odds**successes) * ((1 - odds)**(trials-successes))
    b = factorial(trials) / (factorial(successes)*factorial(trials-successes))
    return a*b


def simulate(_):
    a_heads = 0
    b_heads = 0

    while True:
        flip = bool(random.getrandbits(1))
        if flip:
            a_heads += 1
            if a_heads == 10:
                return True

        flip = bool(random.getrandbits(1))
        if flip:
            b_heads += 1
            if b_heads == 10:
                return False


if __name__ == "__main__":
    # p = Pool()
    # results = p.map(simulate, range(10000000))
    # print(Counter(results))
    odds = list(itertools.accumulate(binomial(0.5, 10, n) for n in range(10, 101)))
    odds_shift = [0] + odds[0:-1]
    odds_diff = [a-b for a, b in zip(odds, odds_shift)]
    plt.plot(*zip(*enumerate(odds_diff)))
    plt.show()
    print("done")

