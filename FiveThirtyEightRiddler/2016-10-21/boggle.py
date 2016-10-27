from enum import IntEnum
from collections import defaultdict
import string
import random
import numpy
from deap import base, creator, tools, algorithms
import multiprocessing

class TrieMembership(IntEnum):
    invalid = 1
    prefix = 2
    word = 3

SCORE_DICT = defaultdict(lambda: 11, {0:0,1:0,2:0,3:1,4:1,5:2,6:3,7:5,8:11})

SIZE = 4
MIN_WORD_LEN = 3

_end = '_end_'

def print_grid(input_list):
    grid = [input_list[i:i + SIZE] for i in range(0, SIZE**2, SIZE)]
    for row in grid:
        print(''.join(row))

def generate_random_boggle_letters():
    return random.choice(string.ascii_lowercase)

def dictionary_gen():
    with open('enable1.txt','r') as word_list:
        for line in word_list:
            yield line.strip()

def neighbors(x,y):
    # range has to be +1 because range is not inclusive on end
    for nx in range(max(0,x-1),min(x+2,SIZE)):
        for ny in range(max(0,y-1),min(y+2,SIZE)):
            yield (nx,ny)

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = '_end_'
    return root

def mutate_grid(individual, indpb):   
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = generate_random_boggle_letters()
    
    return individual,
    
def trie_membership(trie, word):
    current_dict = trie
    for letter in word:
        try:
            current_dict = current_dict[letter]
        except KeyError:
            return TrieMembership.invalid
    if _end in current_dict:
        return TrieMembership.word
    else:
        return TrieMembership.prefix
    
def recurse_grid(input_grid, position, path, current_word, plausible_words_trie):
    found_words = []
    membership = trie_membership(plausible_words_trie,current_word)
    if membership == TrieMembership.word:  
        found_words.append(current_word)
    if membership >= TrieMembership.prefix:
        for nx,ny in neighbors(*position):
            if (nx,ny) not in path:
                new_letter = input_grid[ny][nx]
                new_letter = new_letter if new_letter != 'q' else 'qu'
                new_word = current_word + new_letter
                if trie_membership(plausible_words_trie,new_word) != TrieMembership.invalid:
                    found_words += recurse_grid(input_grid,(nx,ny),path+[(nx,ny)],new_word, plausible_words_trie)
    return found_words
    
def solve_list(input_list):
    return solve(''.join(list(itertools.chain.from_iterable(input_list))))
    
def solve(input_grid):
    # input grid should be groups of 4 letters with spaces between them.
    if len(input_grid) != SIZE**2:
        raise ValueError
    
    grid = [input_grid[i:i + SIZE] for i in range(0, SIZE**2, SIZE)]
    grid_letters = set(input_grid.replace('q','qu').replace(' ',''))
    
    # plausible words are words from the dictionary that only contain
    # letters found in the grid and are more than 3 letters long
    # TODO: this check could be smarter to actually count letters as well.
    plausible_words = [word for word in dictionary_gen() if len(word) > MIN_WORD_LEN and set(word) <= grid_letters]
    plausible_words_trie = make_trie(plausible_words)
    
    found_words = []
    
    for y,row in enumerate(grid):
        for x,letter in enumerate(row):
            found_words += recurse_grid(grid,(x,y),[(x,y)],letter, plausible_words_trie)
    
    score = sum(SCORE_DICT[len(v)] for v in set(found_words))
    return (score,)

def main():
    toolbox = base.Toolbox()
    
    #pool = multiprocessing.Pool()
    #toolbox.register("map", pool.map)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list ,fitness = creator.FitnessMax)

    toolbox.register("rand_letter",generate_random_boggle_letters)
    toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.rand_letter,n=SIZE**2)
    toolbox.register("population",tools.initRepeat,list,toolbox.individual)

    toolbox.register("evaluate",solve_list)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_grid, indpb = 0.15)
    toolbox.register("select",tools.selTournament, tournsize = 4)

    pop = toolbox.population(n=200)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof, verbose=True)
    
    return pop, logbook, hof