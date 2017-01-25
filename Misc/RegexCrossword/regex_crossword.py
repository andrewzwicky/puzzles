import itertools
import re
import deap


class Hex(object):
    def __init__(self, x, z, init_contents):
        self.x = x
        self.y = -x-z
        self.z = z
        self.contents = init_contents

    def __repr__(self):
        return "{:<2},{:<2},{:<2}: {}".format(self.x, self.y, self.z, self.contents)


X_REGEXES = {
    -6: ".*G.*V.*H.*",
    -5: "[CR]*",
    -4: ".*XEXM*",
    -3: ".*DD.*CCM.*",
    -2: ".*XHCR.*X.*",
    -1: ".*(.)(.)(.)(.)\\4\\3\\2\\1.*",
     0: ".*(IN|SE|HI)",
     1: "[^C]*MMM[^C]*",
     2: ".*(.)C\\1X\\1.*",
     3: "[CEIMU]*OH[AEMOR]*",
     4: "(RX|[^R])*",
     5: "[^M]*M[^M]*",
     6: "(S|MM|HHH)*"
}

Y_REGEXES = {
    -6: ".*SE.*UE.*",
    -5: ".*LR.*RL.*",
    -4: ".*OXR.*",
    -3: "([^EMC]|EM)*",
    -2: "(HHX|[^HX])*",
    -1: ".*PRR.*DDC.*",
     0: ".*",
     1: "[AM]*CM(RC)*R?",
     2: "([^MC]|MM|CC)*",
     3: "(E|CR|MN)*",
     4: "P+(..)\\1.*",
     5: "[CHMNOR]*I[CHMNOR]*",
     6: "(ND|ET|IN)[^X]*"
}

Z_REGEXES = {
    -6: ".*H.*H.*",
    -5: "(DI|NS|TH|OM)*",
    -4: "F.*[AO].*[AO].*",
    -3: "(O|RHH|MM)*",
    -2: ".*",
    -1: "C*MC(CCC|MM)*",
     0: "[^C]*[^R]*III.*",
     1: "(...?)\\1*",
     2: "([^X]|XCC)*",
     3: "(RR|HHH)*.?",
     4: "N.*X.X.X.*E",
     5: "R*D*M*",
     6: ".(C|HH)*"
}
    
    
class HexGrid(object):
    def __init__(self, size, x_regexes, y_regexes, z_regexes):
        self.size = size
        self.max_dist = self.size // 2
        self.hexes = [Hex(x, y) for x, y in itertools.product(range(-self.max_dist, self.max_dist+1), repeat=2)
                      if self.cube_distance_hexs(Hex(0, 0), Hex(x, y)) <= self.max_dist]
        self.x_regexes = x_regexes
        self.y_regexes = y_regexes
        self.z_regexes = z_regexes

    @staticmethod
    def cube_distance_hexs(a, b):
        return max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z))

    def get_x_row(self, index):
        # sort by z
        return [h.contents for h in sorted(self.hexes, key=lambda h: -h.z) if h.x == index]

    def get_y_row(self, index):
        # sort by x
        return [h.contents for h in sorted(self.hexes, key=lambda h: -h.x) if h.y == index]

    def get_z_row(self, index):
        # sort by y
        return [h.contents for h in sorted(self.hexes, key=lambda h: -h.y) if h.z == index]
    
    def set_contents(self, x, z, new_contents):
        hex = next((h for h in self.hexes if h.x == x and h.z == z), None)
        if hex is None:
            raise ValueError
        else:
            hex.contents =  new_contents
    
    def validate_x_row(self, index):
        return re.match(self.x_regexes[index], "".join(self.get_x_row(index)))
        
    def validate_y_row(self, index):
        return re.match(self.y_regexes[index], "".join(self.get_y_row(index)))
        
    def validate_z_row(self, index):
        return re.match(self.z_regexes[index], "".join(self.get_z_row(index)))

    def score(self):
        count_x = sum([1 for index in range(-self.max_dist, self.max_dist+1) if self.validate_x_row(index) is not None])
        count_y = sum([1 for index in range(-self.max_dist, self.max_dist+1) if self.validate_y_row(index) is not None])
        count_z = sum([1 for index in range(-self.max_dist, self.max_dist+1) if self.validate_z_row(index) is not None])
        return sum([count_x, count_y, count_z])

        
def generate_random_letter():
    return random.choice(string.ascii_uppercase)
    
    
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
    creator.create("Grid", HexGrid, fitness=creator.FitnessMax)

    toolbox.register("letter", generate_random_letter)
    toolbox.register("individual", tools.initRepeat, creator.Grid, toolbox.letter, n=BOARD_SIZE ** 2)
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
        
if __name__ == "__main__":
    g = HexGrid(13, X_REGEXES, Y_REGEXES, Z_REGEXES)
    
    rows =["NHPEHAS",
    "DIOMOMTH",
    "FOXNXAXPH",
    "MMOMMMMRHH",
    "MCXNMMCRXEM",
    "CMCCCCMMMMMM",
    "HRXRCMIIIHXLS",
    "OREOREOREORE",
    "VCXCCHHMXCC",
    "RRRRHHHRRU",
    "NCXDXEXLE",
    "RRDDMMMM",
    "GCCHHCC"]
    
    rows_iter = itertools.chain.from_iterable(rows)
    
    for z in range(-g.max_dist, g.max_dist+1):
        for x in range(max(-g.max_dist, -z-g.max_dist), min(g.max_dist, -z+g.max_dist)+1):
            g.set_contents(x, z, next(rows_iter))
