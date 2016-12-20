import sys
from collections import namedtuple
from pprint import pprint


def match(circ, jug_h, jug_e, jug_p):
    return circ.h * jug_h + circ.e * jug_e + circ.p * jug_p


def challenge(input_string):
    juggler = namedtuple('juggler', ['h', 'e', 'p', 'des_circuits'])
    circuit = namedtuple('circuit', ['h', 'e', 'p', 'assigned_jugglers'])

    circuits = {}
    jugglers = {}
    for line in input_string:
        if line.startswith('J'):
            j, name, h, e, p, des_circs = line.split(' ')
            H = int(h.replace('H:', ''))
            E = int(e.replace('E:', ''))
            P = int(p.replace('P:', ''))
            circs = des_circs.strip().split(',')
            jugglers[name] = juggler(H, E, P, list(zip(circs, [match(circuits[name], H, E, P) for name in circs])))
        if line.startswith('C'):
            c, name, h, e, p = line.split(' ')
            H = int(h.replace('H:', ''))
            E = int(e.replace('E:', ''))
            P = int(p.replace('P:', ''))
            circuits[name] = circuit(H, E, P, {})

    circuit_scores_sorted = {c_key: [] for c_key in circuits.keys()}

    for name, props in jugglers.items():
        for c_name, score in props.des_circuits:
            circuit_scores_sorted[c_name].append(score)

    for scores in circuit_scores_sorted.values():
        scores = sorted(scores)

    for name_j, juggler in jugglers.items():
        return ','.join(score for name, score in sorted(juggler.des_circuits, key=lambda x: x[0]))


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as test_cases:
        for test in test_cases:
            print(challenge(test))
