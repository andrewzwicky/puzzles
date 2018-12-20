import re
from collections import defaultdict
from copy import copy
from pathlib import Path

data = Path('input.txt').read_text().splitlines()


def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]
    return regs


def addi(a, b, c, regs):
    regs[c] = regs[a] + b
    return regs


def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]
    return regs


def muli(a, b, c, regs):
    regs[c] = regs[a] * b
    return regs


def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]
    return regs


def bani(a, b, c, regs):
    regs[c] = regs[a] & b
    return regs


def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]
    return regs


def bori(a, b, c, regs):
    regs[c] = regs[a] | b
    return regs


def setr(a, _, c, regs):
    regs[c] = regs[a]
    return regs


def seti(a, _, c, regs):
    regs[c] = a
    return regs


def gtir(a, b, c, regs):
    regs[c] = 1 if (a > regs[b]) else 0
    return regs


def gtri(a, b, c, regs):
    regs[c] = 1 if (regs[a] > b) else 0
    return regs


def gtrr(a, b, c, regs):
    regs[c] = 1 if (regs[a] > regs[b]) else 0
    return regs


def eqir(a, b, c, regs):
    regs[c] = 1 if (a == regs[b]) else 0
    return regs


def eqri(a, b, c, regs):
    regs[c] = 1 if (regs[a] == b) else 0
    return regs


def eqrr(a, b, c, regs):
    regs[c] = 1 if (regs[a] == regs[b]) else 0
    return regs


opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri,
           eqrr]
opcode_names = [f.__name__ for i, f in enumerate(opcodes)]
opcode_name_func_map = {k: v for k, v in zip(opcode_names, opcodes)}

data_iter = iter(data)
test_case_num = 0
possibles = defaultdict(set)
counts = defaultdict(list)

while True:
    before = next(data_iter)
    instr = next(data_iter)
    after = next(data_iter)
    _ = next(data_iter)

    if 'Before' not in before:
        break

    else:
        b_registers = list(map(int, re.findall('\d+', before)))
        opcode_num, A, B, C = list(map(int, re.findall('\d+', instr)))
        a_registers = list(map(int, re.findall('\d+', after)))

        for opcode_func in opcodes:
            opcode_result = opcode_func(A, B, C, copy(b_registers))
            if opcode_result == a_registers:
                possibles[opcode_num].add(opcode_func.__name__)
                counts[test_case_num].append(opcode_func.__name__)

    test_case_num += 1

print(len(list(filter(lambda x: len(x) >= 3, counts.values()))))  # Part 1

actuals = dict()
found_opcodes = set()
while len(found_opcodes) < len(opcodes):
    for opcode_num, candidates in possibles.items():
        if len(candidates) == 1:
            found = candidates.pop()
            actuals[opcode_num] = found
            found_opcodes.add(found)
            break

    for opcode_num, candidates in possibles.items():
        possibles[opcode_num] -= found_opcodes

opcode_map = {num: opcode_name_func_map[name] for num, name in actuals.items()}

registers = [0, 0, 0, 0]

while True:
    try:
        line = next(data_iter)
        if line == '':
            continue

        opcode_num, A, B, C = list(map(int, re.findall('\d+', line)))
        registers = opcode_map[opcode_num](A, B, C, copy(registers))
    except StopIteration:
        break

print(registers[0])
