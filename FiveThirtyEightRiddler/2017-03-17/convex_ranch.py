# From Stephen Carrier, a puzzle about domestic boundaries:
# Consider four square-shaped ranches, arranged in a two-by-two pattern,
# as if part of a larger checkerboard. One family lives on each ranch, and
# each family builds a small house independently at a random place within
# the property. Later, as the families in adjacent quadrants become acquainted,
# they construct straight-line paths between the houses that go across the
# boundaries between the ranches, four in total. These paths form a quadrilateral
# circuit path connecting all four houses. This circuit path is also the boundary
# of the area where the families’ children are allowed to roam.
# What is the probability that the children are able to travel in a straight line
# from any allowed place to any other allowed place without leaving the boundaries?
# (In other words, what is the probability that the quadrilateral is convex?)

import random
import matplotlib.pyplot as plt
import itertools


def generate_random_points():
    output = [[random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)] for _ in range(4)]
    output[0][0] -= 1
    output[3][0] -= 1
    output[3][1] -= 1
    output[2][1] -= 1
    return output


def random_simulate():
    points = generate_random_points()

    concave = False

    # http://stackoverflow.com/questions/471962/how-do-determine-if-a-polygon-is-complex-convex-nonconvex

    for i in range(3):
        # start at vertex i and move clockwise
        dx1 = points[(i + 1) % len(points)][0] - points[i % len(points)][0]
        dy1 = points[(i + 1) % len(points)][1] - points[i % len(points)][1]
        dx2 = points[(i + 2) % len(points)][0] - points[(i + 1) % len(points)][0]
        dy2 = points[(i + 2) % len(points)][1] - points[(i + 1) % len(points)][1]
        zcross = dx1 * dy2 - dy1 * dx2
        if zcross > 0:
            concave = True

    # if concave:
    #     fig = plt.figure()
    #     ax = fig.add_subplot(1, 1, 1)
    #
    #     x, y = zip(*points)
    #
    #     ax.scatter(x, y, facecolors='k', s=60)
    #     ax.set_xlim(-1, 1)
    #     ax.set_ylim(-1, 1)
    #
    #     major_ticks = range(0, 2, 1)
    #
    #     ax.set_xticks(major_ticks)
    #     ax.set_yticks(major_ticks)
    #
    #     ax.set_xticklabels([])
    #     ax.set_yticklabels([])
    #
    #     ax.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')
    #
    #     ax.grid(which='both')
    #     plt.show()

    return int(concave)


if __name__ == '__main__':
    count = 10000000

    sums = itertools.accumulate(random_simulate() for _ in range(count))
    mod_sums = [sum / n for n, sum in enumerate(sums, start=1)]
    plt.plot(mod_sums)
