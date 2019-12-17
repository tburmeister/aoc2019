import math
import numpy as np

with open("day15.txt") as fp:
    raw = fp.read()

prog = list(map(int, raw.split(",")))


class Intcode:
    def __init__(self, name, prog):
        self.name = name
        self.prog = [x for x in prog]
        self.pc = 0
        self.rb = 0

    def copy(self):
        new = Intcode(self.name, self.prog)
        new.pc = self.pc
        new.rb = self.rb
        return new

    def get(self, a, mode):
        if mode == 0:
            return self.prog[a]
        if mode == 1:
            return a
        if mode == 2:
            return self.prog[self.rb+a]
        raise Exception("Invalid mode {}".format(mode))

    def set(self, a, x, mode):
        if mode == 0:
            self.ensure(a)
            self.prog[a] = x
        else:
            assert mode == 2
            self.ensure(self.rb+a)
            self.prog[self.rb+a] = x

    def ensure(self, a):
        if a >= len(self.prog):
            k = math.ceil(math.log2(a))
            n = 1 << k
            self.prog.extend([0 for i in range(n - self.prog)])
        
    def run(self, val):
        prog = self.prog
        pc = self.pc
        out = None

        while prog[pc] != 99:
            code = prog[pc]
            op = code % 100
            modes = [(code // 100) % 10, (code // 1000) % 10, (code // 10000) % 10]
            a, b, c = prog[pc+1:pc+4]

            if op == 1:
                x = self.get(a, modes[0]) + self.get(b, modes[1])
                self.set(c, x, modes[2])
                pc += 4
            elif op == 2:
                x = self.get(a, modes[0]) * self.get(b, modes[1])
                self.set(c, x, modes[2])
                pc += 4
            elif op == 3:
                x = val
                # print("{} received {}, mode {}".format(self.name, x, modes[0]))
                self.set(a, x, modes[0])
                pc += 2
            elif op == 4:
                pc += 2
                out = self.get(a, modes[0])
                # print("{} returning {}".format(self.name, out))
                break
            elif op == 5:
                if self.get(a, modes[0]) != 0:
                    pc = self.get(b, modes[1])
                else:
                    pc += 3
            elif op == 6:
                if self.get(a, modes[0]) == 0:
                    pc = self.get(b, modes[1])
                else:
                    pc += 3
            elif op == 7:
                if self.get(a, modes[0]) < self.get(b, modes[1]):
                    self.set(c, 1, modes[2])
                else:
                    self.set(c, 0, modes[2])
                pc += 4
            elif op == 8:
                if self.get(a, modes[0]) == self.get(b, modes[1]):
                    self.set(c, 1, modes[2])
                else:
                    self.set(c, 0, modes[2])
                pc += 4
            elif op == 9:
                self.rb += self.get(a, modes[0])
                pc += 2
            else:
                raise Exception("invalid opcode {}".format(op))

        self.pc = pc
        return out

# breadth first search; copy CPU state and try all possible directions
intcode = Intcode("A", prog)
seen = set()
todo = [(0, 0, 0, intcode)]
start = None

while len(todo) > 0:
    x, y, d, intcode = todo[0]
    todo = todo[1:]
    if (x, y) in seen:
        continue
    seen.add((x, y))

    north = intcode.copy()
    south = intcode.copy()
    west = intcode.copy()
    east = intcode.copy()

    r = north.run(1)
    if r == 2:
        print(d + 1)
        start = north
        break
    if r == 1:
        todo.append((x, y-1, d+1, north))

    r = south.run(2)
    if r == 2:
        print(d + 1)
        start = south
        break
    if r == 1:
        todo.append((x, y+1, d+1, south))

    r = west.run(3)
    if r == 2:
        print(d + 1)
        start = west
        break
    if r == 1:
        todo.append((x-1, y, d+1, west))

    r = east.run(4)
    if r == 2:
        print(d + 1)
        start = east
        break
    if r == 1:
        todo.append((x+1, y, d+1, east))

seen = set()
todo = [(0, 0, 0, start)]
maxd = 0

while len(todo) > 0:
    x, y, d, intcode = todo[0]
    todo = todo[1:]
    if (x, y) in seen:
        continue
    seen.add((x, y))

    if d > maxd:
        maxd = d

    north = intcode.copy()
    south = intcode.copy()
    west = intcode.copy()
    east = intcode.copy()

    r = north.run(1)
    if r == 1:
        todo.append((x, y-1, d+1, north))

    r = south.run(2)
    if r == 1:
        todo.append((x, y+1, d+1, south))

    r = west.run(3)
    if r == 1:
        todo.append((x-1, y, d+1, west))

    r = east.run(4)
    if r == 1:
        todo.append((x+1, y, d+1, east))

print(maxd)

