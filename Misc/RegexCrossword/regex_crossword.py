import itertools
import re


class Hex(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = -x-y
        self.contents = "".join(map(str, [self.x, self.y, self.z]))

    def __repr__(self):
        return "{:<2},{:<2},{:<2}: {}".format(self.x, self.y, self.z, self.contents)


X_REGEXES = {
    -6: ".*G.*V.*H.*",
    -5: "[CR]*",
    -4: ".*XEXM*",
    -3: ".*DD.*CCM.*",
    -2: ".*XHCR.*X.*",
    -1: ".*(.)(.)(.)(.)\4\3\2\1.*",
     0: ".*(IN|SE|HI)",
     1: "[^C]*MMM[^C]*",
     2: ".*(.)C\1X\1.*",
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
     4: "P+(..)\1.*",
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
     1: "(...?)\1*",
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
        return [h.contents for h in sorted(self.hexes, key=lambda h: h.z) if h.x == index]

    def get_y_row(self, index):
        # sort by x
        return [h.contents for h in sorted(self.hexes, key=lambda h: h.x) if h.y == index]

    def get_z_row(self, index):
        # sort by y
        return [h.contents for h in sorted(self.hexes, key=lambda h: h.y) if h.z == index]
    
    def set_contents(self, x, y, new_contents):
        hex = next((h for h in self.hexes if h.x == x and h.y == y), None)
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

if __name__ == "__main__":
    g = HexGrid(13, X_REGEXES, Y_REGEXES, Z_REGEXES)
