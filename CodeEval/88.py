import sys
from collections import namedtuple
from pprint import pprint

sys.argv.append('88_input.txt')

juggler = namedtuple('juggler',['h','e','p','des_circuits'])
circuit = namedtuple('circuit',['h','e','p','assigned_jugglers'])

def match(circuit, jug_h,jug_e,jug_p):
    return circuit.h*jug_h + circuit.e*jug_e + circuit.p*jug_p

with open(sys.argv[1], 'r') as test_case:
    circuits={}
    jugglers={}
    for line in test_case:
        if line.startswith('J'):
            j, name, h, e, p, des_circs = line.split(' ')
            H = int(h.replace('H:',''))
            E = int(e.replace('E:',''))
            P = int(p.replace('P:',''))
            circs = des_circs.strip().split(',')
            jugglers[name]=juggler(H,E,P,list(zip(circs,[match(circuits[name],H,E,P) for name in circs])))
        if line.startswith('C'):
            c, name, h, e, p = line.split(' ')
            H = int(h.replace('H:',''))
            E = int(e.replace('E:',''))
            P = int(p.replace('P:',''))
            circuits[name] = circuit(H,E,P,{})

pprint(jugglers)
pprint(circuits)

circuit_scores_sorted ={c_key:[] for c_key in circuits.keys()}

for name, props in jugglers.items():
	for c_name, score in props.des_circuits:
		circuit_scores_sorted[c_name].append(score)

for scores in circuit_scores_sorted.values():
	scores = sorted(scores)

for name_j, juggler in jugglers.items():
    print([score for name,score in sorted(juggler.des_circuits,key=lambda x: x[0])],',')
