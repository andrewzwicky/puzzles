from boggle import *
import matplotlib.animation as animation

grid_string = "CANEXXDYXXXXXXXX".lower()

fig, line, letters = init_grid_figure(grid_string)

trie = generate_word_trie(grid_string)
grid = generate_grid_list(grid_string)

path_generator = itertools.cycle(recurse_grid(grid, list(), "", trie, set()))

def grid_gen():
    for i in range(10):
        test = [generate_random_boggle_letters() for j in range(16)]

        yield ''.join(test)

# line_ani = animation.FuncAnimation(fig, update_word_line, fargs=(line, path_generator),repeat=True)
# grid_ani = animation.FuncAnimation(fig, update_grid_letter, fargs=(letters, itertools.cycle(grid_gen())),repeat=True)

plt.show()