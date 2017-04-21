import random
from collections import Counter
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def simulate_single_run(num_cards, hand_perc, stop_percentage):
    hand_size = int(num_cards * hand_perc)
    remaining_cards = list(range(1, num_cards + 1))
    hand = random.sample(remaining_cards, hand_size)
    seen_cards = []
    # print(hand, max(hand))
    for num_card, card in enumerate(hand, start=1):
        seen_cards.append(card)
        remaining_cards.remove(card)
        high_card_so_far = max(seen_cards)
        prob_draw_higher_than_highest = len([c for c in remaining_cards if c > high_card_so_far]) / len(remaining_cards)
        prob_any_remaining_higher = 1 - ((1 - prob_draw_higher_than_highest) ** (hand_size - num_card))
        # print(seen_cards, high_card_so_far, prob_draw_higher_than_highest, prob_any_remaining_higher)
        if prob_any_remaining_higher <= stop_percentage:
            return card == max(hand)


def simulate_single_percentage(num_cards, hand_perc, stop_percentage, trials):
    return Counter(simulate_single_run(num_cards, hand_perc, stop_percentage) for _ in range(trials))[True] / trials


def trail_multiple_percentages(num_cards, hand_perc, stop_percentages, trials):
    result = 0
    for pct in stop_percentages:
        result = max(result, simulate_single_percentage(num_cards, hand_perc, pct, trials))

    print(num_cards, hand_perc, result)
    return result


if __name__ == '__main__':
    #NUM_CARDS = np.logspace(2, 5, num=4, dtype=int)
    NUM_CARDS = np.linspace(100, 1000, num=4, dtype=int)
    HAND_PERC = np.linspace(.2, .7, num=6, dtype=float)
    PERCENTAGES = np.linspace(0, 1, num=10, dtype=float)
    SAMPLE_SIZE = 1000

    with Pool(4) as p:
        results = p.starmap(trail_multiple_percentages,
                            [(num_cards, hand_size, PERCENTAGES, SAMPLE_SIZE) for num_cards, hand_size in
                             itertools.product(NUM_CARDS, HAND_PERC)])

    results = np.array(results).reshape((len(NUM_CARDS), len(HAND_PERC))).T
    NUM_CARDS, HAND_PERC = np.meshgrid(NUM_CARDS, HAND_PERC)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(NUM_CARDS, HAND_PERC, results, linewidth=0, antialiased=False, cmap=cm.coolwarm)
    plt.show()
