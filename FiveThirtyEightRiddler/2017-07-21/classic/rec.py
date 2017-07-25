import csv
import itertools
import numpy as np

with open('castle-solutions.csv', newline='', encoding='latin1') as prev_castles_file:
    file_reader = csv.reader(prev_castles_file)
    ARMIES = list(file_reader)

ARMIES = ARMIES[1:]
ARMIES = [tuple(int(n) for n in row[:10]) for row in ARMIES]

TOTAL_SOLDIERS = 100
NUM_CASTLES = 10

POINTS = np.array([1,2,3,4,5,6,7,8,9,10])

def r_min_wrapper(army):
    return r_min((),0,0,(),100,0,army)


def r_min(cur_indx, cur_count, cur_points, best_indx, best_count, best_points, army):
    for i,n in enumerate(army):
        if i not in cur_indx:
            n_count  = cur_count  + n + 1 # must beat by 1 to get points
            n_points = cur_points + POINTS[i]
            n_indx   = cur_indx   + (i,)
            if n_points > 27 and n_count < best_count:
                best_count  = n_count
                best_points = n_points
                best_indx   = n_indx
            elif n_points < 27:
                best_indx, best_count, best_points = r_min(n_indx, n_count, n_points, best_indx, best_count, best_points, army)
    
    return best_indx, best_count, best_points
    
# max_b_c = 0
# for army in ARMIES:
    # b_i, b_c, b_p = r_min((),0,0,(),100,0,army)
    # print(b_c, end='')
    # if b_c > max_b_c:
        # print(army)
        # max_b_c = b_c
    # else:
        # print()
    