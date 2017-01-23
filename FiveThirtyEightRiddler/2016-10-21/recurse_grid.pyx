from enum import IntEnum


BOARD_SIZE = 4
MIN_WORD_LEN = 3
END = '_end_'


class TrieMembership(IntEnum):
    invalid = 1
    prefix = 2
    word = 3


def dictionary_gen():
    with open('../../enable1.txt', 'r') as word_list:
        for line in word_list:
            yield line.upper().strip()


def neighbors(x, y):
    if not 0 <= x < BOARD_SIZE or not 0 <= y < BOARD_SIZE:
        raise ValueError("square not within board")

    """
    x is the x index of the supplied square.  To cover squares to
    the left and right, we should go from x-1 to x+1.  Because
    the range() function is not inclusive on the upper bound,
    we'll need to go to x+2.

    To prevent returning squares that are outside the board, the
    range should be capped at 0 and BOARD_SIZE.
    """

    lower_x = max(0, x - 1)
    upper_x = min(x + 2, BOARD_SIZE)

    lower_y = max(0, y - 1)
    upper_y = min(y + 2, BOARD_SIZE)

    for nx in range(lower_x, upper_x):
        for ny in range(lower_y, upper_y):
            yield (nx, ny)


def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[END] = END
    return root

ALL_WORD_TRIE = make_trie(word for word in dictionary_gen() if len(word) > MIN_WORD_LEN)

TRIE_MEMBERS = dict()


def recurse_grid(grid):
    for (path, word) in recurse_grid_internal(grid, list(), "", ALL_WORD_TRIE, set()):
        yield (path, word)


def recurse_grid_internal(grid, path, current_word, words_trie, found_words):
    if not path:  # empty path means this is the initial call.
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                for (next_path, next_word) in recurse_grid_internal(grid, [(x, y)], letter, words_trie, found_words):
                    yield (next_path, next_word)

        return
    position = path[-1]
    membership = trie_member(words_trie, current_word)
    if membership == TrieMembership.word and current_word not in found_words:
        found_words.add(current_word)
        yield (path, current_word)
    if membership >= TrieMembership.prefix:
        for nx, ny in neighbors(*position):
            if (nx, ny) not in path:
                new_letter = grid[ny][nx]
                new_letter = new_letter if new_letter != 'q' else 'qu'
                new_word = current_word + new_letter
                if trie_member(words_trie, new_word) != TrieMembership.invalid:
                    for (next_path, next_word) in recurse_grid_internal(grid,
                                                                        list(path) + [(nx, ny)],
                                                                        new_word,
                                                                        words_trie,
                                                                        found_words):
                        yield (next_path, next_word)


def trie_member(trie, word):
    try:
        return TRIE_MEMBERS[word]
    except KeyError:
        current_dict = trie
        for letter in word:
            try:
                current_dict = current_dict[letter]
            except KeyError:
                TRIE_MEMBERS[word] = TrieMembership.invalid
                return TRIE_MEMBERS[word]
        if END in current_dict:
            TRIE_MEMBERS[word] = TrieMembership.word
            return TRIE_MEMBERS[word]
        else:
            TRIE_MEMBERS[word] = TrieMembership.prefix
            return TRIE_MEMBERS[word]
