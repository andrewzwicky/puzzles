import re


juggler_re = re.compile("J J(\d) H:(\d) E:(\d) P:(\d) ((C\d,?)+)")
circuit_re = re.compile("C C(\d) H:(\d) E:(\d) P:(\d)")


class Juggler(object):
    def __init__(self, i, h, e, p, desired_circuits):
        self.id = i
        self.h = h
        self.e = e
        self.p = p
        self.desired_circuits = desired_circuits
        self.scores = []

    def __repr__(self):
        return "{{{} {} {} {} {}}}".format(self.h, self.e, self.p, [c.id for c in self.desired_circuits], self.scores)

    def score(self):
        self.scores = [match(circuit, self) for circuit in self.desired_circuits]

    def print_scores(self):
        circ_scores = ' '.join(
            "C{}:{}".format(circ.id, score) for circ, score in zip(self.desired_circuits, self.scores))
        return "J{} {}".format(self.id, circ_scores)

    def circuit_index(self, circuit):
        return self.desired_circuits.index(circuit)


class Circuit(object):
    def __init__(self, i, h, e, p, assigned_jugglers=None):
        self.id = i
        self.h = h
        self.e = e
        self.p = p
        if assigned_jugglers is None:
            self.assigned_jugglers = []
        else:
            self.assigned_jugglers = assigned_jugglers

    def __repr__(self):
        return "{} {} {} {}".format(self.h, self.e, self.p, self.assigned_jugglers)

    def print_scores(self):
        jugg_scores = ', '.join(jugg.print_scores() for jugg in self.assigned_jugglers)
        return "C{} {}".format(self.id, jugg_scores)

    def get_juggler_scores(self):
        return [j.scores[j.circuit_index(self)] for j in self.assigned_jugglers]


def match(circuit, juggler):
    return circuit.h * juggler.h + circuit.e * juggler.e + circuit.p * juggler.p


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
        juggler = sorted(jugglers, key=lambda x: max(x.scores))[0]
        circ_index = juggler.scores.index(max(juggler.scores))
        juggler.desired_circuits[circ_index].assigned_jugglers.append(juggler)
        jugglers.remove(juggler)

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

    circuits.sort(key=lambda x: x.id)
    jugglers.sort(key=lambda x: x.id)

    for juggler in jugglers:
        juggler.desired_circuits = [circuits[i] for i in juggler.desired_circuits]
        juggler.score()

    circuits = perform_assignments(jugglers, circuits)

    return circuits
