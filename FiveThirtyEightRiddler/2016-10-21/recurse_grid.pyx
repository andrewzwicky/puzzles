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
            # capitalize all words for consistency, and strip newline character off the end
            yield line.upper().strip()


def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            # as the letters get counted, traverse further into the dict
            # if the key does not exist, it will be created.  Otherwise
            # current_dict will just move deeper into the dictionary
            current_dict = current_dict.setdefault(letter, {})
        # add the END key at the deepest level to signal that this string is a word
        current_dict[END] = END
    return root

ALL_WORD_TRIE = make_trie(word for word in dictionary_gen() if len(word) > MIN_WORD_LEN)

TRIE_MEMBERS = dict()


def trie_member(trie, word):
    # try to fetch the membership from the list in memory first.
    try:
        return TRIE_MEMBERS[word]

    # if the word has not been tested already, calculate whether the string
    # is not a valid word/prefix, whether it is a prefix to possible words
    # or a word itself.
    except KeyError:
        current_dict = trie
        for letter in word:
            try:
                # attempt to follow the letters through the trie dict
                current_dict = current_dict[letter]
            except KeyError:
                # once a key is not found, this means there is no longer a valid
                TRIE_MEMBERS[word] = TrieMembership.invalid
                return TRIE_MEMBERS[word]
        if END in current_dict:
            TRIE_MEMBERS[word] = TrieMembership.word
            return TRIE_MEMBERS[word]
        else:
            TRIE_MEMBERS[word] = TrieMembership.prefix
            return TRIE_MEMBERS[word]


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





def recurse_grid(grid):
    for (path, word) in recurse_grid_internal(grid, list(), "", ALL_WORD_TRIE, set()):
        yield (path, word)


def recurse_grid_internal(grid, path, current_word, words_trie, found_words):
    # path should be empty on the initial call
    if not path:
        # This is the initial call to ensure that we start a search from each square in the grid.
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                for (next_path, next_word) in recurse_grid_internal(grid, [(x, y)], letter, words_trie, found_words):
                    yield (next_path, next_word)

        return
    # path is a list of squares, so the last one in the list is our current position in the grid
    current_position = path[-1]

    # test to see how our word is contained in the word list
    membership = trie_member(words_trie, current_word)

    # We have found a new word from our list and should yield the current path and the word
    if membership == TrieMembership.word and current_word not in found_words:
        found_words.add(current_word)
        yield (path, current_word)

    # If it's not a full word, but a prefix to one or more words in the list, continue searching by moving
    # to a neighbor and adding that letter to the current word.
    if membership >= TrieMembership.prefix:
        for nx, ny in neighbors(*current_position):
            # the same square can only be used in each word once
            if (nx, ny) not in path:
                new_letter = grid[ny][nx]

                # the Q cube in boggle has QU on it.
                new_letter = new_letter if new_letter != 'q' else 'qu'

                # add the letter on the newest cube to the current word.
                new_word = current_word + new_letter

                # if the new word is either a word or prefix, continue recursively searching from that new square.
                if trie_member(words_trie, new_word) != TrieMembership.invalid:
                    for (next_path, next_word) in recurse_grid_internal(grid,
                                                                        list(path) + [(nx, ny)],
                                                                        new_word,
                                                                        words_trie,
                                                                        found_words):
                        yield (next_path, next_word)


