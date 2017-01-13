import sys
import re

juggler_re = re.compile("J J(\d+) H:(\d+) E:(\d+) P:(\d+) ((C\d+,?)+)")
circuit_re = re.compile("C C(\d+) H:(\d+) E:(\d+) P:(\d+)")


class Juggler(object):
    def __init__(self, i, h, e, p, des_circuits):
        self.i = i
        self.h = h
        self.e = e
        self.p = p
        self.des_circuits = des_circuits
        self.scores = []

    def __repr__(self):
        return "J{}({})".format(self.i, ",".join("{}:{}".format(c.i, score) for c, score in zip(self.des_circuits, self.scores)))

    @staticmethod
    def _match(circuit, juggler):
        return circuit.h * juggler.h + circuit.e * juggler.e + circuit.p * juggler.p

    def score(self):
        self.scores = [self._match(circuit, self) for circuit in self.des_circuits]

    def circuit_index(self, circuit):
        return self.des_circuits.index(circuit)

    def circuit_score(self, circuit):
        return self.scores[self.circuit_index(circuit)]


class Circuit(object):
    def __init__(self, i, h, e, p, assigned_jugglers=None):
        self.i = i
        self.h = h
        self.e = e
        self.p = p
        if assigned_jugglers is None:
            self.assigned_jugglers = []
        else:
            self.assigned_jugglers = assigned_jugglers

    def __repr__(self):
        return "C{} {}".format(self.i, self.assigned_jugglers)

    def print_scores(self):
        jugg_scores = ', '.join(jugg.print_scores() for jugg in self.assigned_jugglers)
        return "C{} {}".format(self.i, jugg_scores)

    def get_juggler_scores(self):
        return [j.scores[j.circuit_index(self)] for j in self.assigned_jugglers]


def parse_line(line):
    jugg_match = juggler_re.match(line)
    circuit_match = circuit_re.match(line)

    if jugg_match:
        i = int(jugg_match.group(1))
        h = int(jugg_match.group(2))
        e = int(jugg_match.group(3))
        p = int(jugg_match.group(4))
        circuits = list(map(int, jugg_match.group(5).replace("C", "").split(',')))
        return Juggler(i, h, e, p, circuits)

    if circuit_match:
        i = int(circuit_match.group(1))
        h = int(circuit_match.group(2))
        e = int(circuit_match.group(3))
        p = int(circuit_match.group(4))
        return Circuit(i, h, e, p)


def swap_jugglers(circuits):
    for circuit in circuits:
        for this_juggler in circuit.assigned_jugglers:
            more_prefered_circuits = this_juggler.des_circuits[0:this_juggler.circuit_index(circuit)]
            for pref_circuit in more_prefered_circuits:
                for other_juggler in pref_circuit.assigned_jugglers:
                    if other_juggler.circuit_score(pref_circuit) < this_juggler.circuit_score(pref_circuit):
                        pref_circuit.assigned_jugglers.remove(other_juggler)
                        circuit.assigned_jugglers.append(other_juggler)
                        circuit.assigned_jugglers.remove(this_juggler)
                        pref_circuit.assigned_jugglers.append(this_juggler)
                        return True, circuits
    return False, circuits


def perform_assignments(jugglers, circuits):
    """
    In fact we want to match jugglers to circuits such that no juggler could switch
    to a circuit that they prefer more than the one they are assigned to and be a
    better fit for that circuit than one of the other jugglers assigned to it."
    """
    num_circuits = len(circuits)
    num_jugglers = len(jugglers)
    jugglers_per_circuit = num_jugglers // num_circuits

    while jugglers:
        top_juggler = sorted(jugglers, key=lambda x: tuple(x.scores))[0]
        for circuit, score in zip(top_juggler.des_circuits, top_juggler.scores):
            if len(circuit.assigned_jugglers) < jugglers_per_circuit:
                circuit.assigned_jugglers.append(top_juggler)
                jugglers.remove(top_juggler)
                break
            else:
                lower_pref_jugglers = [juggler for juggler in circuit.assigned_jugglers if juggler.circuit_index(circuit) > top_juggler.circuit_index(circuit)]
                for other_juggler in lower_pref_jugglers:
                    if top_juggler.circuit_score(circuit) > other_juggler.circuit_score(circuit):
                        circuit.assigned_jugglers.remove(other_juggler)
                        jugglers.append(other_juggler)
                        circuit.assigned_jugglers.append(top_juggler)
                        jugglers.remove(top_juggler)
                        break

    swapping = True

    while swapping:
        swapping, circuits = swap_jugglers(circuits)

    for circuit in circuits:
        circuit.assigned_jugglers.sort(key=lambda j: j.i)

    circuits.sort(key=lambda c: c.i)

    return circuits


def challenge(input_string):
    jugglers = []
    circuits = []

    for line in input_string.split("\n"):
        output = parse_line(line)
        if type(output) == Circuit:
            circuits.append(output)
        if type(output) == Juggler:
            jugglers.append(output)

    circuits.sort(key=lambda x: x.i)
    jugglers.sort(key=lambda x: x.i)

    for juggler in jugglers:
        juggler.des_circuits = [circuits[i] for i in juggler.des_circuits]
        juggler.score()

    circuits = perform_assignments(jugglers, circuits)

    return circuits

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        test = test_cases.read()

    circuits = challenge(test)
    C1970 = next((x for x in circuits if x.i == 1970), None)
    print(sum(j.i for j in C1970.assigned_jugglers))
