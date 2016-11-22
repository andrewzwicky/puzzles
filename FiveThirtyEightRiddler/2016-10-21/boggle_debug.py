from boggle import *
import matplotlib.animation as animation

pop, logbook, hof = simulate(population=10000,
                             generations=50,
                             individual_mutate_prob=.7,
                             mating_prob=0.7,
                             letter_mutate_prob=0.4,
                             tournament_size=10)

grid_fig, grid_line, grid_letters, grid_anns = init_grid_figure()

grids = [generation['best'] for generation in logbook.chapters['boards']]


def prop_gen(logbook_arg):
    grid_strings = [b['best'] for b in logbook_arg.chapters['boards']]
    maxes = [b['max'] for b in logbook_arg.chapters['scores']]
    generations = itertools.count()

    for s, m, g in zip(grid_strings, maxes, generations):
        yield {'new_grid': s,
               'new_score': m,
               'new_generation': g}


grid_ani = animation.FuncAnimation(grid_fig, update_grid,
                                   fargs=(grid_line, grid_letters, grid_anns, itertools.cycle(prop_gen(logbook))),
                                   repeat=True)
grid_ani.save("evolve_animation.gif", writer="imagemagick", fps=4)

best_grid_string = grids[-1]
path_fig, path_line, path_letters, path_anns = init_grid_figure(best_grid_string)
grid = generate_grid_list(best_grid_string)
data = [(path, word) for path, word in recurse_grid(grid, list(), "", ALL_WORD_TRIE, set())]


def generate_path(data_arg, gen):
    total_score = 0
    for path, word in data_arg:
        total_score += LEN_TO_SCORE[len(word)]
        yield {'new_generation': gen,
               'new_word_coords': path,
               'new_score': total_score,
               'new_word': word}


line_ani = animation.FuncAnimation(path_fig, update_grid, frames=len(data), fargs=(
    path_line, path_letters, path_anns, itertools.cycle(generate_path(data, len(grids)))), repeat=True)
line_ani.save("path_animation.gif", writer="imagemagick", fps=10)