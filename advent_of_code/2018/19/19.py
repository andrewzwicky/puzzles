import re
from pathlib import Path

data = Path('input.txt').read_text().splitlines()


# data = Path('test.txt').read_text().splitlines()


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


def eqir(a, b, c, regs):
    regs[c] = 1 if (a == regs[b]) else 0


def eqri(a, b, c, regs):
    regs[c] = 1 if (regs[a] == b) else 0


def eqrr(a, b, c, regs):
    regs[c] = 1 if (regs[a] == regs[b]) else 0


data_iter = iter(data)
ip = int(re.search('\d+', next(data_iter)).group(0))

instructions = []
for i in data_iter:
    name, *args = i.split(' ')
    args = list(map(int, args))
    instructions.append((eval(name), args))

registers = [0, 0, 0, 0, 0, 0]

while True:
    instruction = registers[ip]
    try:
        func, args = instructions[instruction]
        func(*args, registers)
        registers[ip] += 1
    except IndexError:
        break

print(registers[0])

registers = [1, 0, 0, 0, 0, 0]

while True:
    instruction = registers[ip]
    try:
        func, args = instructions[instruction]
        func(*args, registers)
        registers[ip] += 1
    except IndexError:
        break

print(registers[0])
