from pathlib import Path
import re
import numpy as np

data = Path('input.txt').read_text().splitlines()

def addr(a, b, c, regs): regs[c] = regs[a] + regs[b]
def addi(a, b, c, regs): regs[c] = regs[a] + b
def mulr(a, b, c, regs): regs[c] = regs[a] * regs[b]
def muli(a, b, c, regs): regs[c] = regs[a] * b
def banr(a, b, c, regs): regs[c] = regs[a] & regs[b]
def bani(a, b, c, regs): regs[c] = regs[a] & b
def borr(a, b, c, regs): regs[c] = regs[a] | regs[b]
def bori(a, b, c, regs): regs[c] = regs[a] | b
def setr(a, _, c, regs): regs[c] = regs[a]
def seti(a, _, c, regs): regs[c] = a
def gtir(a, b, c, regs): regs[c] = 1 if (a > regs[b]) else 0
def gtri(a, b, c, regs): regs[c] = 1 if (regs[a] > b) else 0
def gtrr(a, b, c, regs): regs[c] = 1 if (regs[a] > regs[b]) else 0
def eqir(a, b, c, regs): regs[c] = 1 if (a == regs[b]) else 0
def eqri(a, b, c, regs): regs[c] = 1 if (regs[a] == b) else 0
def eqrr(a, b, c, regs): regs[c] = 1 if (regs[a] == regs[b]) else 0
    


data_iter = iter(data)
ip = int(re.search('\d+', next(data_iter)).group(0))

instructions = []
for i in data_iter:
    line = re.search('\w{4} \d+ \d+ \d+', i).group(0)
    name, *args = line.split(' ')
    args = list(map(int, args))
    instructions.append((eval(name), args))

registers = [0, 0, 0, 0, 0, 0]
count = 0

last_5 = [0,0,0,0,0]
cycle = []


while True:
    instruction = registers[ip]
    try:
        if instruction == 28:
            last_5 = tuple(last_5[1:]) + (registers[5],)
            if last_5 in cycle:
                print(last_5)
                break
            cycle.append(last_5)
            print(registers)
        func, args = instructions[instruction]
        func(*args, registers)
        registers[ip] += 1
    except IndexError:
        break

    count += 1

print(registers[0])