from enum import IntEnum
import os

BOARD_SIZE = 4
MIN_WORD_LEN = 3
END = '_end_'
NUM = '_num_'


class TrieMembership(IntEnum):
    invalid = 1
    prefix = 2
    word = 3


def dictionary_gen():
    file_name = os.path.relpath(os.path.join("..", "..", "enable1.txt"))
    with open(file_name, 'r') as word_list:
        for line in word_list:
            # capitalize all words for consistency, and strip newline character off the end
            yield line.upper().strip()


def make_trie(words):
    current_node_number = 0
    # start with an empty dictionary
    root = dict()
    # the base node will be node 0
    # each node will have a unique number assigned
    # to it that is used for drawing the graph later
    root[NUM] = current_node_number
    current_node_number += 1

    for word in words:
        # for each word, the addition of the letter nodes
        # needs to start at the root level again
        current_dict = root
        for letter in word:
            # if the node for this letter doesn't exist yet, create
            # and empty dictionary there
            if letter not in current_dict:
                current_dict[letter] = {}

            # as the letters get counted, traverse further into the dict
            # to add the nodes for all the letters
            current_dict = current_dict[letter]

            # if this node does not have a number already
            # add one and increment the counter
            if NUM not in current_dict:
                current_dict[NUM] = current_node_number
                current_node_number += 1

        # add the END key at the deepest node for this word
        # to signal that this string is a word.
        current_dict[END] = END
    return root


ALL_WORD_TRIE = make_trie(word for word in dictionary_gen() if len(word) >= MIN_WORD_LEN)

# This is a cache of all the lookups so far, to speed up repeated queries to the trie.
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
                # once a key is not found, this means this word is not in the trie
                TRIE_MEMBERS[word] = TrieMembership.invalid
                return TRIE_MEMBERS[word]
        if END in current_dict:
            # If END is found, this string is a full word in our original dictionary
            TRIE_MEMBERS[word] = TrieMembership.word
            return TRIE_MEMBERS[word]
        else:
            # If all letters are still in the trie, but this is not a full word,
            # it means there are words that start with this string.
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


def recurse_grid_external(grid, full_output=False):
    if type(grid) is not list:
        raise ValueError("grid must be a list")
    for result in recurse_grid_internal(grid, list(), "", ALL_WORD_TRIE, set(), full_output):
        yield result


def recurse_grid_internal(grid, path, current_word, words_trie, found_words, full_output=False):
    # path should be empty on the initial call
    if not path:
        # This is the initial call to ensure that a search
        # starts from each square in the grid.
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                for next_result in recurse_grid_internal(grid,
                                                         [(x, y)],
                                                         letter,
                                                         words_trie,
                                                         found_words,
                                                         full_output):
                    yield next_result

        return
    # path is a list of coordinates, so the last one
    # in the list is our current position in the grid
    current_position = path[-1]

    # test to see how our word is contained in the word list
    membership = trie_member(words_trie, current_word)
    if full_output:
        yield (path, current_word, membership)
    # We have found a new word from our list and
    # should yield the current path and the word
    if membership == TrieMembership.word and current_word not in found_words:
        found_words.add(current_word)
        if not full_output:
            yield (path, current_word, membership)

    # If it's not a full word, but a prefix to one or more words in the
    # list, continue searching by moving to a neighbor
    # and adding that letter to the current word.
    if membership >= TrieMembership.prefix:
        for nx, ny in neighbors(*current_position):
            # the same square can only be used in each word once
            if (nx, ny) not in path:
                new_letter = grid[ny][nx]

                # the Q cube in boggle has QU on it.
                new_letter = new_letter if new_letter != 'q' else 'qu'

                # add the letter on the newest cube to the current word.
                new_word = current_word + new_letter

                # continue recursively searching from the next square.
                for next_result in recurse_grid_internal(grid,
                                                         path + [(nx, ny)],
                                                         new_word,
                                                         words_trie,
                                                         found_words,
                                                         full_output):
                    yield next_result
