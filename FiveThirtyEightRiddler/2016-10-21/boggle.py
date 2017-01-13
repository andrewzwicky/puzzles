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


# noinspection PyArgumentList
LEN_TO_SCORE = defaultdict(lambda: 11, {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 5, 8: 11})

GEN_KEY = 'Gen'
SCORE_KEY = 'Score'
WORD_KEY = 'Word'

ANNOT_FORMAT = "{name}: {value}"

'''
Grid starts with (0,0) in the top left corner.
X is column
Y is row
'''


def init_grid_figure(input_string=None):
    if not input_string:
        input_string = "                "

    input_string = input_string.upper()

    fig = plt.figure(figsize=(5, 6))
    ax = fig.add_axes([0, 0, 1, 1], axisbg='#E6E3DB')

    ax.set_ylim(0, BOARD_SIZE)
    ax.set_xlim(0, BOARD_SIZE)
    ax.grid(True, linestyle="-", linewidth=2)

    loc = plt.MultipleLocator(base=1)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)

    plt.gca().set_aspect('equal', adjustable='box')

    text_size = 15

    annotations = {GEN_KEY: ax.text(0, 4.2, "", size=text_size),
                   SCORE_KEY: ax.text(1.35, 4.2, "", size=text_size),
                   WORD_KEY: ax.text(2.4, 4.2, "", size=text_size)}

    pos1 = ax.get_position()  # get the original position
    pos2 = [0, 0, pos1.width, pos1.height]
    ax.set_position(pos2)  # set a new position

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    letter_color = "#0495A8"

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

    return fig, line, letters, annotations


def update_grid_fig(line,
                    letters,
                    annotations,
                    new_word_coords=None,
                    new_grid=None,
                    new_generation=None,
                    new_score=None,
                    new_word=None):
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


def update_grid(_, line, letters, anns, update_dict_generator):
    output = next(update_dict_generator)
    return update_grid_fig(line, letters, anns, **output)


def word_coord_to_plot_coord(coord):
    x, y = coord
    return x + 0.5, BOARD_SIZE - y - 0.5


def neighbors(x, y):
    # range has to be +1 because range is not inclusive on end
    for nx in range(max(0, x - 1), min(x + 2, BOARD_SIZE)):
        for ny in range(max(0, y - 1), min(y + 2, BOARD_SIZE)):
            yield (nx, ny)


def generate_grid_list(grid_string):
    grid_string = ''.join(grid_string).upper()
    return [grid_string[i:i + BOARD_SIZE] for i in range(0, BOARD_SIZE ** 2, BOARD_SIZE)]


def total_grid_score(grid_string):
    grid_string = ''.join(grid_string).upper()

    grid = generate_grid_list(grid_string)

    words = set(word for _, word in recurse_grid(grid))

    return sum(LEN_TO_SCORE[word_len] for word_len in map(len, words)),


def generate_random_boggle_letters():
    return random.choice(string.ascii_uppercase)


def mutate_grid(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = generate_random_boggle_letters()

    return individual,


def prop_gen(logbook_arg):
    grid_strings = [b['best'] for b in logbook_arg.chapters['boards']]
    maxes = [b['max'] for b in logbook_arg.chapters['scores']]
    generations = itertools.count()

    for s, m, g in zip(grid_strings, maxes, generations):
        yield {'new_grid': s,
               'new_score': m,
               'new_generation': g}


def generate_path(data_arg, gen):
    total_score = 0
    for path, word in data_arg:
        total_score += LEN_TO_SCORE[len(word)]
        yield {'new_generation': gen,
               'new_word_coords': path,
               'new_score': total_score,
               'new_word': word}


def generate_path_gif(logbook, output_file):
    grids = [generation['best'] for generation in logbook.chapters['boards']]
    best_grid_string = grids[-1]
    path_fig, path_line, path_letters, path_anns = init_grid_figure(best_grid_string)
    grid = generate_grid_list(best_grid_string)
    data = [(path, word) for path, word in recurse_grid(grid)]
    line_ani = animation.FuncAnimation(path_fig, update_grid, frames=len(data), fargs=(
        path_line, path_letters, path_anns, itertools.cycle(generate_path(data, len(grids)))), repeat=True)
    line_ani.save(output_file, writer="imagemagick", fps=10)


def generate_evolution_gif(logbook, output_file):
    grid_fig, grid_line, grid_letters, grid_anns = init_grid_figure()

    grid_ani = animation.FuncAnimation(grid_fig, update_grid,
                                       fargs=(grid_line, grid_letters, grid_anns, itertools.cycle(prop_gen(logbook))),
                                       repeat=True)
    grid_ani.save(output_file, writer="imagemagick", fps=4)


def get_best_board(stats):
    fit_values = [ind.fitness.values[0] for ind in stats]
    index = fit_values.index(max(fit_values))
    return ''.join(stats[index])


def get_num_unique_boards(stats):
    return len(set(''.join(ind) for ind in stats))


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
    best_stats.register("best", get_best_board)
    best_stats.register("uniq", get_num_unique_boards)

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
