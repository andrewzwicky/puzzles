import itertools
from pathlib import Path

data = Path('input.txt').read_text().splitlines()

adjustments = list(map(int, data))
print(sum(adjustments))  # Part 1


def find_first_repeat(sequence):
    seen_freqs = set()

    for result in itertools.accumulate(itertools.cycle(sequence)):
        if result not in seen_freqs:
            seen_freqs.add(result)
            continue
        return result


print(find_first_repeat(adjustments))  # Part 2

print()
