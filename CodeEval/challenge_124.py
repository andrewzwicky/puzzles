import sys


def challenge(input_string):
    city_dist = [tuple(dest.split(',')) for dest in input_string.rstrip(';').split('; ')]
    cities, dists = zip(*city_dist)
    #dists_int = sorted(list(map(ints, dists)))
    # cities_dist_ints = list(zip(cities,dists_int))
    # result = sorted(cities_dist_ints,key = lambda tup: tup[1])
    print()


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))