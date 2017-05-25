# coding: utf-8

# In[1]:

import csv
import itertools
from deap import base, creator, tools, algorithms
import random
import numpy as np

# In[21]:

with open('castle-solutions.csv', newline='', encoding='latin1') as prev_castles_file:
    file_reader = csv.reader(prev_castles_file)
    ARMIES = list(file_reader)

ARMIES = ARMIES[1:]
ARMIES = [tuple(int(n) for n in row[:10]) for row in ARMIES]

TOTAL_SOLDIERS = 100
NUM_CASTLES = 10

POINTS = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


# In[27]:

def normalize_army(army):
    army_sum = sum(army)

    for troop in army:
        troop = int((troop / army_sum) * TOTAL_SOLDIERS)

    army_sum = sum(army)

    if army_sum < TOTAL_SOLDIERS:
        army[army.index(min(army))] += TOTAL_SOLDIERS - army_sum
    if army_sum > TOTAL_SOLDIERS:
        army[army.index(max(army))] -= army_sum - TOTAL_SOLDIERS

    return army


# In[4]:

def generate_random_army():
    army = [random.randint(0, TOTAL_SOLDIERS) for _ in range(NUM_CASTLES)]
    return normalize_army(army)


# In[5]:

def total_castles_defeated(army):
    wins = 0

    for other_army in ARMIES:
        castle_diffs = np.subtract(army, other_army)

        other_sum = np.sum(POINTS[np.argwhere(castle_diffs < 0)])
        army_sum = np.sum(POINTS[np.argwhere(castle_diffs > 0)])
        # split points don't matter to winning

        if army_sum > other_sum:
            wins += 1

    return wins,


# In[6]:

def mate_armies(army1, army2):
    new_army1, new_army2 = tools.cxTwoPoint(army1, army2)

    new_army1 = normalize_army(new_army1)
    new_army2 = normalize_army(new_army2)

    return new_army1, new_army2


# In[12]:

def mutate_army(army, indpb):
    if random.random() < indpb:
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        while a != b and army[b] > 0:
            b = random.randint(0, 9)

        army[a] += 1
        army[b] -= 1

    return army,


# In[13]:

def get_best_army(stats):
    fit_values = [army.fitness.values[0] for army in stats]
    index = fit_values.index(max(fit_values))
    return stats[index]


# In[14]:

def get_num_unique_armies(stats):
    return len(set(map(tuple, stats)))


# In[15]:

def init_individual(army_container):
    return army_container(generate_random_army())


# In[28]:

def simulate(population=200,
             generations=20,
             tournament_size=20,
             mating_prob=0.5,
             individual_mutate_prob=0.2,
             hof_size=1):
    toolbox = base.Toolbox()

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Army", list, fitness=creator.FitnessMax)

    toolbox.register("individual", init_individual, creator.Army)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", total_castles_defeated)
    toolbox.register("mate", mate_armies)
    toolbox.register("mutate", mutate_army, indpb=individual_mutate_prob)
    toolbox.register("select", tools.selTournament, tournsize=tournament_size)

    pop = toolbox.population(n=population)
    hof = tools.HallOfFame(hof_size)

    stats = tools.Statistics(lambda army: army.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    best_stats = tools.Statistics(lambda army: army)
    best_stats.register("best", get_best_army)
    best_stats.register("uniq", get_num_unique_armies)

    all_stats = tools.MultiStatistics(scores=stats, boards=best_stats)

    pop, logbook = algorithms.eaSimple(pop,
                                       toolbox,
                                       mating_prob,
                                       individual_mutate_prob,
                                       generations,
                                       stats=all_stats,
                                       halloffame=hof,
                                       verbose=True)

    return pop, logbook, hof


# In[29]:

p, l, h = simulate(population=1000, generations=20)
