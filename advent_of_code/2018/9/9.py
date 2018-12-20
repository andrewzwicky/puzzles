import itertools
import re
from pathlib import Path

import numpy as np

data = Path('input.txt').read_text().strip()

players, last_marble = map(int, re.findall('\d+', data))


def calculate(players, last_marble):
    result = np.array([0, 2, 1])
    last_placed_index = 1
    scores = np.zeros(players)

    for player, marble_num in zip(itertools.cycle(np.roll(np.array(range(players)), -len(result))),
                                  range(max(result) + 1, last_marble + 1)):
        if marble_num % 23 != 0:
            new_index = last_placed_index + 2
            if new_index == len(result):
                result = np.append(result, marble_num)
            else:
                new_index = new_index % len(result)
                result = np.insert(result, new_index, marble_num)

            last_placed_index = int(np.where(result == marble_num)[0][0])

        else:
            new_index = (len(result) + last_placed_index - 7) % len(result)
            scores[player] += marble_num
            scores[player] += result[new_index]
            result = np.delete(result, new_index)
            last_placed_index = new_index


    print(int(max(scores)))  # Part 1

calculate(players, last_marble)
# TODO: identify the pattern here
calculate(players, last_marble * 100)
