import itertools


class Hex(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = -x-y
        self.contents = "".join(map(str, [self.x, self.y, self.z]))

    def __repr__(self):
        return "{:<2},{:<2},{:<2}: {}".format(self.x, self.y, self.z, self.contents)


X_REGEXES = [
    ".*H.*H.*",
    "(DI|NS|TH|OM)*",
    "F.*[AO].*[AO].*",
    "(O|RHH|MM)*",
    ".*",
    "C*MC(CCC|MM)*",
    "[^C]*[^R]*III.*",
    "(...?)\1*",
    "([^X]|XCC)*",
    "(RR|HHH)*.?",
    "N.*X.X.X.*E",
    "R*D*M*",
    ".(C|HH)*"
]

Y_REGEXES = [
    ".*H.*H.*",
    "(DI|NS|TH|OM)*",
    "F.*[AO].*[AO].*",
    "(O|RHH|MM)*",
    ".*",
    "C*MC(CCC|MM)*",
    "[^C]*[^R]*III.*",
    "(...?)\1*",
    "([^X]|XCC)*",
    "(RR|HHH)*.?",
    "N.*X.X.X.*E",
    "R*D*M*",
    ".(C|HH)*"
]

Z_REGEXES = [
    ".*H.*H.*",
    "(DI|NS|TH|OM)*",
    "F.*[AO].*[AO].*",
    "(O|RHH|MM)*",
    ".*",
    "C*MC(CCC|MM)*",
    "[^C]*[^R]*III.*",
    "(...?)\1*",
    "([^X]|XCC)*",
    "(RR|HHH)*.?",
    "N.*X.X.X.*E",
    "R*D*M*",
    ".(C|HH)*"
]
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
        return [h.contents for h in sorted(self.hexes, key=lambda h: h.z) if h.x == index]

    def get_y_row(self, index):
        # sort by x
        return [h.contents for h in sorted(self.hexes, key=lambda h: h.x) if h.y == index]

    def get_z_row(self, index):
        # sort by y
        return [h.contents for h in sorted(self.hexes, key=lambda h: h.y) if h.z == index]

if __name__ == "__main__":
    g = HexGrid(13)

