import pyximport

pyximport.install()
from collections import defaultdict
import string
import random
from deap import base, creator, tools
import matplotlib.pyplot as plt
import numpy
import itertools
from recurse_grid import recurse_grid
from recurse_grid import BOARD_SIZE
import matplotlib.animation as animation
import networkx
from boggle import *
from recurse_grid import ALL_WORD_TRIE, trie_member, TrieMembership





def update_trie_grid_fig(line, path, graph, graph_axes, current_word, membership):
    x, y = zip(*list(map(word_coord_to_plot_coord, path)))

    line.set_xdata(x)
    line.set_ydata(y)

    nodes =[0]
    root = NODE_TRIE
    for letter in current_word:
        try:
            nodes.append(root[letter]["num"])
            root = root[letter]
        except KeyError:
            break

    networkx.draw_networkx_nodes(graph, ax=graph_axes, pos=POS, node_size=450, node_color="w", nodelist=graph.nodes())

    color = ""
    if membership == TrieMembership.invalid:
        color = "r"
    elif membership == TrieMembership.word:
        color = "g"
    else:
        color = "y"

    line.set_color(color)
    networkx.draw_networkx_nodes(graph, ax=graph_axes, pos=POS, node_size=450, node_color=color, nodelist=nodes)

    plt.draw()


def update_trie_fig(_, line, graph, graph_axes, update_dict_generator):
    path, current_word, membership = next(update_dict_generator)
    return update_trie_grid_fig(line, path, graph, graph_axes, current_word, membership)





def recurse_grid_internal(grid, path, current_word, words_trie, found_words, debug=False):
    # path should be empty on the initial call
    if not path:
        # This is the initial call to ensure that a search
        # starts from each square in the grid.
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                for this in recurse_grid_internal(grid,
                                                  [(x, y)],
                                                  letter,
                                                  words_trie,
                                                  found_words,
                                                  debug):
                    yield tuple(this)

        return
    # path is a list of coordinates, so the last one
    # in the list is our current position in the grid
    current_position = path[-1]

    # test to see how our word is contained in the word list
    membership = trie_member(words_trie, current_word)
    if debug:
        yield (path, current_word, membership)
    # We have found a new word from our list and
    # should yield the current path and the word
    if membership == TrieMembership.word and current_word not in found_words:
        found_words.add(current_word)
        if not debug:
            yield (path, current_word)

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

                # if the new word is either a word or prefix,
                # continue recursively searching from that new square.

                for this in recurse_grid_internal(grid,
                                                  path + [(nx, ny)],
                                                  new_word,
                                                  words_trie,
                                                  found_words,
                                                  debug):
                    yield tuple(this)


if __name__ == "__main__":
    generate_trie_gif("trie.gif")
