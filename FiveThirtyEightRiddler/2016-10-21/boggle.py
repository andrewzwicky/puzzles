import pyximport;

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
from recurse_grid import recurse_grid_external, BOARD_SIZE, NUM, TrieMembership, make_trie, END
import matplotlib.animation as animation
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import re
import os

# region axis population methods
GEN_KEY = 'Gen'
SCORE_KEY = 'Score'
WORD_KEY = 'Word'

ANNOT_FORMAT = "{name}: {value}"

GRAPH_KWARGS = {"font_size": 12, "node_size": 350}


def init_boggle_board_axis(ax, input_string):
    letter_color = "#0495A8"
    text_size = 15

    input_string = input_string.upper()

    ax.set_axis_bgcolor('#E6E3DB')

    [sp.set_visible(False) for sp in ax.spines.values()]
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


def init_trie_axis(ax, edges, node_to_letter):
    graph = nx.Graph(list(edges))
    pos = graphviz_layout(graph, prog='dot')
    # nx.draw_networkx(graph, ax=ax, pos=pos, labels=node_to_letter, node_color="w", edge_color='k', **GRAPH_KWARGS)

    [sp.set_visible(False) for sp in ax.spines.values()]
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')
    return graph, pos


# endregion

# region figure generation methods
def boggle_board_only_figure(input_string=None):
    if input_string is None:
        input_string = ' ' * BOARD_SIZE ** 2
    fig = plt.figure(figsize=(5, 6))
    ax = fig.add_axes([0, 0, 1, 1])

    line, letters, annotations = init_boggle_board_axis(ax, input_string)

    return fig, line, letters, annotations


def boggle_trie_figure(input_string, edges, node_to_letter):
    fig = plt.figure(figsize=(12, 6), facecolor="#FFFFFF")
    board_axis = plt.subplot2grid((1, 2), (0, 0), axisbg='#E6E3DB')
    trie_axis = plt.subplot2grid((1, 2), (0, 1))

    line, letters, annotations = init_boggle_board_axis(board_axis, input_string)
    graph, pos = init_trie_axis(trie_axis, edges, node_to_letter)

    plt.subplots_adjust(wspace=0, hspace=0)

    return fig, line, letters, annotations, trie_axis, graph, pos


# endregion

# region animation figure update methods
def update_animation_figure_wrapper(frame_num, line, letters, annotations, graph, graph_axis, node_to_letter,
                                    update_dict_generator):
    output = next(update_dict_generator)
    update_boggle_axis(line, letters, annotations, **output)
    if graph is not None:
        update_trie_axis(graph, graph_axis, node_to_letter, **output)


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


def update_trie_axis(graph, graph_axis, node_to_letter, word_nodes, membership=None, pos=None, trie=None, new_word=None,
                     **kwargs):
    if membership is None or trie is None or new_word is None or pos is None:
        raise ValueError

    nodes = [0]
    root = trie
    for letter in new_word:
        try:
            nodes.append(root[letter][NUM])
            root = root[letter]
        except KeyError:
            break

    for _ in range(len(graph_axis.collections)):
        del graph_axis.collections[0]

    for _ in range(len(graph_axis.texts)):
        del graph_axis.texts[0]

    plt.draw()

    if membership == TrieMembership.invalid:
        color = "r"
    elif membership == TrieMembership.word:
        color = "g"
    else:
        color = "y"

    node_colors = [color if node in nodes else 'w' for node in graph.nodes()]
    edge_colors = [color if edge in list(zip(nodes, nodes[1:])) else 'k' for edge in graph.edges()]
    linewidths = [2 if n in word_nodes else 1 for n in graph.nodes()]

    nx.draw_networkx(graph, ax=graph_axis, pos=pos, labels=node_to_letter, linewidths=linewidths,
                     node_color=node_colors,
                     edge_color=edge_colors,
                     **GRAPH_KWARGS)

# endregion

# region animation helper methods
def word_coord_to_plot_coord(coord):
    x, y = coord
    return x + 0.5, BOARD_SIZE - y - 0.5


def get_trie_information(trie, edges, word_nodes, nodes_to_letters):
    for key in trie:
        if key not in [END, NUM]:
            edges.add((trie[NUM], trie[key][NUM]))
            nodes_to_letters[trie[key][NUM]] = key
            get_trie_information(trie[key], edges, word_nodes, nodes_to_letters)

    if END in trie:
        word_nodes.add(trie[NUM])

    return edges, word_nodes, nodes_to_letters


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
    words = set(word for _, word, _ in recurse_grid_external(grid))

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
    data = [(path, word, membership) for path, word, membership in recurse_grid_external(best_grid)]
    line_ani = animation.FuncAnimation(fig,
                                       update_animation_figure_wrapper,
                                       frames=len(data),
                                       fargs=(line,
                                              letters,
                                              annotations,
                                              None,
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
                                              None,
                                              itertools.cycle(generate_evolution_annotations(logbook))),
                                       repeat=True)
    grid_ani.save(output_file, writer="imagemagick", fps=4)


def generate_trie_gif(logbook, output_file):
    frame_limit = 300
    best_grid_string = logbook.chapters['boards'][-1]['best']
    best_grid = transform_grid_string_to_list(best_grid_string)
    data = [(path, word, membership) for path, word, membership in recurse_grid_external(best_grid, full_output=True)]
    grid_words = [word for path, word, membership in data[:frame_limit] if membership == TrieMembership.word]
    this_grid_trie = make_trie(grid_words)
    edges, word_nodes, nodes_to_letters = get_trie_information(this_grid_trie, set(), set(), dict())
    fig, line, letters, annotations, graph_axis, graph, pos = boggle_trie_figure(best_grid_string, edges,
                                                                                 nodes_to_letters)
    grid_ani = animation.FuncAnimation(fig,
                                       update_animation_figure_wrapper,
                                       fargs=(line,
                                              letters,
                                              annotations,
                                              graph,
                                              graph_axis,
                                              nodes_to_letters,
                                              itertools.cycle(
                                                  generate_trie_annotations(data[:frame_limit], this_grid_trie, pos))),
                                       repeat=True)
    grid_ani.save(output_file, writer="imagemagick", fps=1)
    print("done")


def generate_final_board(logbook, output_file):
    best_grid_string = logbook.chapters['boards'][-1]['best']
    fig, line, letters, annotations = boggle_board_only_figure(best_grid_string)
    plt.savefig(output_file)


def generate_generation_scores(logbook, output_file):
    top_scores = [gen['max'] for gen in logbook.chapters['scores']]
    avg_scores = [gen['avg'] for gen in logbook.chapters['scores']]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('top score of each generation')
    plt.plot(range(len(top_scores)), top_scores, color='r')
    plt.plot(range(len(avg_scores)), avg_scores, color='k-')
    ax.set_xlabel('generation')
    ax.set_ylabel('score')

    plt.savefig(output_file, facecolor='w')


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

    if checkpoint is None:
        toolbox.register("letter", generate_random_boggle_letters)
        toolbox.register("individual", tools.initRepeat, creator.Board, toolbox.letter, n=BOARD_SIZE ** 2)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", total_grid_score)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", mutate_grid, indpb=letter_mutate_prob)
        toolbox.register("select", tools.selTournament, tournsize=tournament_size)

        pop = toolbox.population(n=population)
        hof = tools.HallOfFame(hof_size)

    else:
        pop = None
        hof = None

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
    if False:
        pickle_files = [f for f in os.listdir('pickles') if f.startswith('gen')]
        if pickle_files:
            highest_gen_file = os.path.join('pickles',
                                            max(pickle_files, key=lambda x: int(re.match(".*_(\d+)_.*", x).group(1))))
        else:
            highest_gen_file = None
        print(highest_gen_file)
        p, l, h = simulate(population=1000000, generations=100, checkpoint=highest_gen_file)
        generate_evolution_gif(l, "evo.gif")
        generate_path_gif(l, "path.gif")
        generate_trie_gif(l, "trie.gif")
        generate_final_board(l, "final_board.png")
        generate_generation_scores(l, "scores_over_time.png")
    else:
        words = ["a", "about", "above", "across", "act", "active", "activity", "cake", "call", "can", "candle", "keep",
                 "kin","key", "kill", "kind", "king"]
        fig = plt.figure(figsize=(6, 4))
        graph_axis = fig.add_axes([0, 0, 1, 1])
        trie = make_trie(map(lambda x: x.upper(), words))
        e, word_nodes, node_to_letter = get_trie_information(trie, set(), set(), dict())
        graph, pos = init_trie_axis(graph_axis, e, node_to_letter)
        update_trie_axis(graph, graph_axis, node_to_letter, word_nodes=word_nodes, membership=TrieMembership.word,
                         pos=pos, trie=trie,
                         new_word="")
        plt.savefig("../../../andrewzwicky.github.io/img/posts/boggle_solver/example_trie.png")
        update_trie_axis(graph, graph_axis, node_to_letter, word_nodes=word_nodes, membership=TrieMembership.word,
                         pos=pos, trie=trie,
                         new_word="KIN")
        plt.savefig("../../../andrewzwicky.github.io/img/posts/boggle_solver/example_trie_1.png")
        update_trie_axis(graph, graph_axis, node_to_letter, word_nodes=word_nodes, membership=TrieMembership.word,
                         pos=pos, trie=trie,
                         new_word="KIND")
        plt.savefig("../../../andrewzwicky.github.io/img/posts/boggle_solver/example_trie_2.png")
        update_trie_axis(graph, graph_axis, node_to_letter, word_nodes=word_nodes, membership=TrieMembership.word,
                         pos=pos, trie=trie,
                         new_word="KING")
        plt.savefig("../../../andrewzwicky.github.io/img/posts/boggle_solver/example_trie_3.png")


# todo: line between trie and boggle board is goofy
# todo: generation is messed up on path gif
# todo: try to space out nodes more on trie gif
# todo: trie gif includes lots of paths that aren't in the trie (prefixes?)
