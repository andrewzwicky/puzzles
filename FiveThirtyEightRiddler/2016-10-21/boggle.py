import pyximport

pyximport.install()
from collections import defaultdict
import string
import random
from deap import base, creator, tools
from deap.algorithms import varAnd
import pickle
import matplotlib.pyplot as plt
import numpy
import itertools
from recurse_grid import recurse_grid, BOARD_SIZE, TrieMembership
import matplotlib.animation as animation
import networkx as nx

# region axis population methods
GEN_KEY = 'Gen'
SCORE_KEY = 'Score'
WORD_KEY = 'Word'

ANNOT_FORMAT = "{name}: {value}"


def init_boggle_board_axis(ax, input_string):
    letter_color = "#0495A8"
    text_size = 15

    input_string = input_string.upper()

    ax.set_axis_bgcolor('#E6E3DB')

    ax.set_ylim(0, BOARD_SIZE)
    ax.set_xlim(0, BOARD_SIZE)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, linestyle="-", linewidth=2)

    loc = plt.MultipleLocator(base=1)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)

    plt.gca().set_aspect('equal', adjustable='box')

    annotations = {GEN_KEY: ax.text(0, 4.2, "", size=text_size),
                   SCORE_KEY: ax.text(1.35, 4.2, "", size=text_size),
                   WORD_KEY: ax.text(2.4, 4.2, "", size=text_size)}

    pos1 = ax.get_position()  # get the original position
    pos2 = [0, 0, pos1.width, pos1.height]
    ax.set_position(pos2)  # set a new position

    letters = [ax.annotate(letter,
                           xy=(y + 0.5, x + 0.5),
                           xycoords='data',
                           ha="center",
                           va="center",
                           size=40,
                           color=letter_color,
                           zorder=1) for letter, (x, y) in
               zip(input_string, itertools.product(reversed(range(BOARD_SIZE)), range(BOARD_SIZE)))]

    line, = ax.plot([],
                    [],
                    '-',
                    color="black",
                    linewidth=50,
                    zorder=2,
                    alpha=0.15,
                    solid_capstyle='round')

    plt.draw()

    return line, letters, annotations


def init_trie_axis(ax, edges, pos, node_to_letter):
    graph = nx.Graph(edges)
    nx.draw_networkx_nodes(graph, ax=ax, pos=pos, node_size=450, node_color="w", nodelist=graph.nodes())
    nx.draw_networkx_labels(graph, pos, node_to_letter, font_size=14)
    nx.draw_networkx_edges(graph, pos)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')
    return graph


# endregion

# region figure generation methods
def boggle_board_only_figure(input_string=None):
    if input_string is None:
        input_string = ' ' * BOARD_SIZE ** 2
    fig = plt.figure(figsize=(5, 6))
    ax = fig.add_axes([0, 0, 1, 1])

    line, letters, annotations = init_boggle_board_axis(ax, input_string)

    return fig, line, letters, annotations


def boggle_trie_figure(input_string, edges, pos, node_to_letter):
    fig = plt.figure(figsize=(12, 6), facecolor="#FFFFFF")
    board_axis = plt.subplot2grid((1, 2), (0, 0), axisbg='#E6E3DB')
    trie_axis = plt.subplot2grid((1, 2), (0, 1))

    line, letters, annotations = init_boggle_board_axis(board_axis, input_string)
    graph = init_trie_axis(trie_axis, edges, pos, node_to_letter)

    plt.subplots_adjust(wspace=0, hspace=0)

    return fig, line, letters, annotations, trie_axis, graph


# endregion

# region animation figure update methods
def update_animation_figure_wrapper(_, line, letters, annotations, graph, graph_axis, update_dict_generator):
    output = next(update_dict_generator)
    update_boggle_axis(line, letters, annotations, **output)
    if graph is not None:
        update_trie_axis(graph, graph_axis, **output)


def update_boggle_axis(line,
                       letters,
                       annotations=None,
                       new_word_coords=None,
                       new_grid=None,
                       new_generation=None,
                       new_score=None,
                       new_word=None,
                       **kwargs):
    if new_generation is not None:
        annotations[GEN_KEY].set_text(ANNOT_FORMAT.format(name=GEN_KEY, value=new_generation))

    if new_score is not None:
        annotations[SCORE_KEY].set_text(ANNOT_FORMAT.format(name=SCORE_KEY, value=new_score))

    if new_word is not None:
        annotations[WORD_KEY].set_text(ANNOT_FORMAT.format(name=WORD_KEY, value=new_word))

    if new_grid is not None:
        new_grid = new_grid.upper()
        for letter, new_letter in zip(letters, new_grid):
            letter.set_text(new_letter)

    if new_word_coords is not None:
        x, y = zip(*list(map(word_coord_to_plot_coord, new_word_coords)))

        line.set_xdata(x)
        line.set_ydata(y)

    plt.draw()


def update_trie_axis(graph, graph_axis, membership=None, trie=None, pos=None, new_word=None, **kwargs):
    if membership is None or trie is None or pos is None or new_word is None:
        raise ValueError

    nodes = [0]
    root = trie
    for letter in new_word:
        try:
            nodes.append(root[letter]["num"])
            root = root[letter]
        except KeyError:
            break

    nx.draw_networkx_nodes(graph, ax=graph_axis, pos=pos, node_size=450, node_color="w", nodelist=graph.nodes())

    if membership == TrieMembership.invalid:
        color = "r"
    elif membership == TrieMembership.word:
        color = "g"
    else:
        color = "y"

    nx.draw_networkx_nodes(graph, ax=graph_axis, pos=pos, node_size=450, node_color=color, nodelist=nodes)
    plt.draw()

# endregion

# region animation helper methods
def word_coord_to_plot_coord(coord):
    x, y = coord
    return x + 0.5, BOARD_SIZE - y - 0.5


def generate_path_annotations(data_arg, gen):
    total_score = 0
    for path, word, membership in data_arg:
        total_score += LEN_TO_SCORE[len(word)]
        yield {'new_generation': gen,
               'new_word_coords': path,
               'new_score': total_score,
               'new_word': word}


def generate_evolution_annotations(logbook_arg):
    grid_strings = [b['best'] for b in logbook_arg.chapters['boards']]
    maxes = [b['max'] for b in logbook_arg.chapters['scores']]
    generations = itertools.count()

    for s, m, g in zip(grid_strings, maxes, generations):
        yield {'new_grid': s,
               'new_score': m,
               'new_generation': g}


def generate_trie_annotations(data_arg, trie, pos):
    for path, word, membership in data_arg:
        yield {'membership': membership,
               'new_word_coords': path,
               'new_word': word,
               'trie': trie,
               'pos': pos}

# endregion

# region simulation helper methods
# noinspection PyArgumentList
LEN_TO_SCORE = defaultdict(lambda: 11, {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 5, 8: 11})


def total_grid_score(grid_string):
    grid_string = ''.join(grid_string).upper()
    grid = transform_grid_string_to_list(grid_string)
    words = set(word for _, word, _ in recurse_grid(grid))

    return sum(LEN_TO_SCORE[word_len] for word_len in map(len, words)),


def transform_grid_string_to_list(grid_string):
    grid_string = ''.join(grid_string).upper()
    return [grid_string[i:i + BOARD_SIZE] for i in range(0, BOARD_SIZE ** 2, BOARD_SIZE)]


def generate_random_boggle_letters():
    return random.choice(string.ascii_uppercase)


def mutate_grid(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = generate_random_boggle_letters()

    return individual,


# endregion

# region gif generation methods
def generate_path_gif(logbook, output_file):
    best_grid_string = logbook.chapters['boards'][-1]['best']
    fig, line, letters, annotations = boggle_board_only_figure(best_grid_string)
    best_grid = transform_grid_string_to_list(best_grid_string)
    data = [(path, word, membership) for path, word, membership in recurse_grid(best_grid)]
    line_ani = animation.FuncAnimation(fig,
                                       update_animation_figure_wrapper,
                                       frames=len(data),
                                       fargs=(line,
                                              letters,
                                              annotations,
                                              None,
                                              None,
                                              itertools.cycle(generate_path_annotations(data, len(data)))),
                                       repeat=True)

    line_ani.save(output_file, writer="imagemagick", fps=10)


def generate_evolution_gif(logbook, output_file):
    fig, line, letters, annotations = boggle_board_only_figure()

    grid_ani = animation.FuncAnimation(fig,
                                       update_animation_figure_wrapper,
                                       fargs=(line,
                                              letters,
                                              annotations,
                                              None,
                                              None,
                                              itertools.cycle(generate_evolution_annotations(logbook))),
                                       repeat=True)
    grid_ani.save(output_file, writer="imagemagick", fps=4)


def generate_trie_gif(logbook, output_file):
    # region data
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
    # endregion

    # best_grid_string = logbook.chapters['boards'][-1]['best']
    best_grid_string = "ASH PEX TOL     "
    fig, line, letters, annotations, graph_axis, graph = boggle_trie_figure(best_grid_string, EDGES, POS, NODE_TO_LETTER)
    best_grid = transform_grid_string_to_list(best_grid_string)
    data = [(path, word, membership) for path, word, membership in recurse_grid(best_grid)]
    grid_ani = animation.FuncAnimation(fig,
                                       update_animation_figure_wrapper,
                                       fargs=(line,
                                              letters,
                                              annotations,
                                              graph,
                                              graph_axis,
                                              itertools.cycle(generate_trie_annotations(data, NODE_TRIE, POS))),
                                       repeat=True)
    grid_ani.save(output_file, writer="imagemagick", fps=4)


# endregion

# region stats methods
def stats_get_best_board(stats):
    fit_values = [ind.fitness.values[0] for ind in stats]
    index = fit_values.index(max(fit_values))
    return ''.join(stats[index])


def stats_get_num_unique_boards(stats):
    return len(set(''.join(ind) for ind in stats))


# endregion

# region updated checkpointing algorithm
# noinspection PyPep8Naming
def eaSimpleCheckpointing(population, toolbox, cxpb, mutpb, ngen, checkpoint=None, stats=None, halloffame=None,
                          verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param checkpoint: A checkpoint file to reload from.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population and a :class:`~deap.tools.Logbook`
              with the statistics of the evolution.

    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution (if
    any). The logbook will contain the generation number, the number of
    evalutions for each generation and the statistics if a
    :class:`~deap.tools.Statistics` if any. The *cxpb* and *mutpb* arguments
    are passed to the :func:`varAnd` function. The pseudocode goes as follow
    ::

        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
            evaluate(offspring)
            population = offspring

    As stated in the pseudocode above, the algorithm goes as follow. First, it
    evaluates the individuals with an invalid fitness. Second, it enters the
    generational loop where the selection procedure is applied to entirely
    replace the parental population. The 1:1 replacement ratio of this
    algorithm **requires** the selection procedure to be stochastic and to
    select multiple times the same individual, for example,
    :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
    Third, it applies the :func:`varAnd` function to produce the next
    generation population. Fourth, it evaluates the new individuals and
    compute the statistics on this population. Finally, when *ngen*
    generations are done, the algorithm returns a tuple with the final
    population and a :class:`~deap.tools.Logbook` of the evolution.

    .. note::

        Using a non-stochastic selection method will result in no selection as
        the operator selects *n* individuals from a pool of *n*.

    This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """

    if checkpoint:
        cp = pickle.load(open(checkpoint, "rb"))
        logbook = cp['logbook']
        population = cp['population']
        toolbox = cp['toolbox']
        cxpb = cp['cxpb']
        mutpb = cp['mutpb']
        start_gen = cp['generation'] + 1  # start on the next generation
        halloffame = cp['halloffame']
    else:
        start_gen = 1
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if halloffame is not None:
            halloffame.update(population)

        record = stats.compile(population) if stats else {}
        logbook.record(gen=0, nevals=len(invalid_ind), **record)

    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(start_gen, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        # Fill the dictionary using the dict(key=value[, ...]) constructor
        cp = dict(population=population,
                  generation=gen,
                  halloffame=halloffame,
                  logbook=logbook,
                  rndstate=random.getstate(),
                  toolbox=toolbox,
                  cxpb=cxpb,
                  mutpb=mutpb)
        pickle.dump(cp, open("pickles/gen_{}_dump.pkl".format(gen), "wb"))

    return population, logbook


# endregion

# region simulation
def simulate(population=200,
             generations=20,
             letter_mutate_prob=0.25,
             tournament_size=20,
             mating_prob=0.5,
             individual_mutate_prob=0.2,
             hof_size=1,
             checkpoint=None):
    toolbox = base.Toolbox()

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Board", list, fitness=creator.FitnessMax)

    toolbox.register("letter", generate_random_boggle_letters)
    toolbox.register("individual", tools.initRepeat, creator.Board, toolbox.letter, n=BOARD_SIZE ** 2)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", total_grid_score)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_grid, indpb=letter_mutate_prob)
    toolbox.register("select", tools.selTournament, tournsize=tournament_size)

    pop = toolbox.population(n=population)
    hof = tools.HallOfFame(hof_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    best_stats = tools.Statistics(lambda ind: ind)
    best_stats.register("best", stats_get_best_board)
    best_stats.register("uniq", stats_get_num_unique_boards)

    all_stats = tools.MultiStatistics(scores=stats, boards=best_stats)

    pop, logbook = eaSimpleCheckpointing(pop,
                                         toolbox,
                                         cxpb=mating_prob,
                                         mutpb=individual_mutate_prob,
                                         ngen=generations,
                                         stats=all_stats,
                                         halloffame=hof,
                                         checkpoint=checkpoint,
                                         verbose=True)

    return pop, logbook, hof


# endregion

if __name__ == "__main__":
    p, l, h = simulate(population=20, generations=5)
    #generate_evolution_gif(l, "evo.gif")
    #generate_path_gif(l, "path.gif")
    generate_trie_gif(l, "trie.gif")
