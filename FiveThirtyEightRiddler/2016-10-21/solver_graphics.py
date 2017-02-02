import pyximport

pyximport.install()
from collections import defaultdict
import string
import random
from deap import base, creator, tools
from eaSimpleCheckpointing import eaSimpleCheckpointing
import matplotlib.pyplot as plt
import numpy
import itertools
from recurse_grid import recurse_grid
from recurse_grid import BOARD_SIZE
import matplotlib.animation as animation
import networkx
from boggle import *
from recurse_grid import ALL_WORD_TRIE, trie_member, TrieMembership

EDGES = [(0, 1),
         (0, 2),
         (1, 3),
         (1, 4),
         (2, 5),
         (2, 6),
         (2, 7),
         (2, 8),
         (3, 9),
         (3, 10),
         (4, 11),
         (4, 12),
         (4, 13),
         (5, 14),
         (5, 15),
         (6, 16),
         (6, 17),
         (6, 18),
         (6, 19),
         (6, 20),
         (7, 21),
         (8, 22),
         (8, 23),
         (11, 24),
         (11, 25),
         (12, 26),
         (15, 27),
         (27, 32),
         (18, 28),
         (21, 29),
         (22, 30),
         (23, 31),
         (32, 33)]

POS = {0: (8, 6),
             1: (3, 5),
             2: (8, 2),
             3: (1, 4),
             4: (4, 4),
             5: (4, 1),
             6: (7, 1),
             7: (10, 1),
             8: (12, 1),
             9: (0, 3),
             10: (1, 3),
             11: (3, 3),
             12: (4, 3),
             13: (5, 3),
             14: (3, 0),
             15: (4, 0),
             16: (5, 0),
             17: (6, 0),
             18: (7, 0),
             19: (8, 0),
             20: (9, 0),
             21: (10, 0),
             22: (11, 0),
             23: (12, 0),
             24: (2, 2),
             25: (3, 2),
             26: (4, 2),
             27: (4, -1),
             28: (7, -1),
             29: (10, -1),
             30: (11, -1),
             31: (12, -1),
             32: (4, -2),
             33: (4, -3)}

NODE_TO_LETTER = {0: '',
           1: 'A',
           2: 'S',
           3: 'S',
           4: 'P',
           5: 'A',
           6: 'E',
           7: 'H',
           8: 'P',
           9: 'H',
           10: 'P',
           11: 'E',
           12: 'S',
           13: 'T',
           14: 'E',
           15: 'P',
           16: 'A',
           17: 'L',
           18: 'P',
           19: 'T',
           20: 'X',
           21: 'E',
           22: 'A',
           23: 'O',
           24: 'S',
           25: 'X',
           26: 'E',
           27: 'O',
           28: 'T',
           29: 'A',
           30: 'E',
           31: 'T',
           32: 'T',
           33: 'E'}

NODE_TRIE = {'A': {'P': {'E': {'S': {'_end_': '_end_', 'num': 24},
                          'X': {'_end_': '_end_', 'num': 24},
                          '_end_': '_end_',
                          'num': 11},
                    'S': {'E': {'_end_': '_end_', 'num': 26}, 'num': 12},
                    'T': {'_end_': '_end_', 'num': 13},
                    'num': 4},
              'S': {'H': {'_end_': '_end_', 'num': 9},
                    'P': {'_end_': '_end_', 'num': 10},
                    'num': 3},
              'num': 1},
        'S': {'A': {'E': {'_end_': '_end_', 'num': 14},
                    'P': {'O': {'T': {'E': {'_end_': '_end_', 'num': 33}, 'num': 32},
                                'num': 27},
                          '_end_': '_end_',
                          'num': 15},
                    'num': 5},
              'E': {'A': {'_end_': '_end_', 'num': 16},
                    'L': {'_end_': '_end_', 'num': 17},
                    'P': {'T': {'_end_': '_end_', 'num': 28}, 'num': 18},
                    'T': {'_end_': '_end_', 'num': 19},
                    'X': {'_end_': '_end_', 'num': 20},
                    'num': 6},
              'H': {'E': {'A': {'_end_': '_end_', 'num': 29},
                          '_end_': '_end_',
                          'num': 21},
                    'num': 7},
              'P': {'A': {'E': {'_end_': '_end_', 'num': 30},
                          '_end_': '_end_',
                          'num': 22},
                    'O': {'T': {'_end_': '_end_', 'num': 31}, 'num': 23},
                    'num': 8},
              'num': 2}}


def trie_grid_figure(input_string):
    fig = plt.figure(figsize=(12, 6), facecolor="#FFFFFF")
    ax1 = plt.subplot2grid((1, 2), (0, 0), axisbg='#E6E3DB')
    ax2 = plt.subplot2grid((1, 2), (0, 1))

    plt.subplots_adjust(wspace=0, hspace=0)

    G = networkx.Graph(EDGES)
    networkx.draw_networkx_nodes(G, ax=ax2, pos=POS, node_size=450, node_color="w", nodelist=G.nodes())
    networkx.draw_networkx_labels(G, POS, NODE_TO_LETTER, font_size=14)
    networkx.draw_networkx_edges(G, POS)

    ax1.set_ylim(0, BOARD_SIZE)
    ax1.set_xlim(0, BOARD_SIZE)

    ax1.grid(True, linestyle="-", linewidth=2)

    loc = plt.MultipleLocator(base=1)
    ax1.xaxis.set_major_locator(loc)
    ax1.yaxis.set_major_locator(loc)

    fig.tight_layout(h_pad=0, w_pad=0, pad=0)

    plt.gca().set_aspect('equal', adjustable='box')

    ax1.set_xticklabels([])
    ax1.set_yticklabels([])

    ax2.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')

    ax2.set_xticklabels([])
    ax2.set_yticklabels([])

    letter_color = "#0495A8"

    letters = [ax1.annotate(letter,
                            xy=(y + 0.5, x + 0.5),
                            xycoords='data',
                            ha="center",
                            va="center",
                            size=90,
                            color=letter_color,
                            zorder=1) for letter, (x, y) in
               zip(input_string, itertools.product(reversed(range(BOARD_SIZE)), range(BOARD_SIZE)))]

    line, = ax1.plot([],
                     [],
                     '-',
                     color="black",
                     linewidth=60,
                     zorder=2,
                     alpha=0.15,
                     solid_capstyle='round')

    plt.draw()

    return fig, line, G, ax2


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


def generate_trie_gif(output_file):
    gif_frames = 100
    input_string = "ASHPEXTOL"
    path_fig, path_line, graph, graph_axes = trie_grid_figure(input_string)
    grid = generate_grid_list(input_string)
    data = []
    for path, word, membership in recurse_grid_internal(grid, list(), "", ALL_WORD_TRIE, set(), debug=True):
        data.append((path, word, membership))
    print([w for p, w, m in data[0:gif_frames] if m == TrieMembership.word])
    line_ani = animation.FuncAnimation(path_fig, update_trie_fig, frames=gif_frames,
                                       fargs=(path_line, graph, graph_axes, itertools.cycle(data[0:gif_frames])), repeat=True)
    line_ani.save(output_file, writer="imagemagick", fps=1)


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
