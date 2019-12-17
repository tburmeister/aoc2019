import math
import numpy as np

with open("day17.txt") as fp:
    raw = fp.read()

prog = list(map(int, raw.split(",")))


class Intcode:
    def __init__(self, name, prog):
        self.name = name
        self.prog = [x for x in prog] + [0, 0, 0]
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
            k = math.ceil(math.log2(a + 1))
            n = 1 << k
            self.prog.extend([0 for i in range(n - len(self.prog))])
        
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
                x = val[0]
                val = val[1:]
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
                raise Exception("invalid opcode {} at pc {}".format(op, pc))

        self.pc = pc
        return out

# breadth first search; copy CPU state and try all possible directions
intcode = Intcode("A", prog)
row = []
out = [row]
while True:
    ret = intcode.run(0)
    if ret is None:
        break
    if chr(ret) == "\n":
        row = []
        out.append(row)
    else:
        row.append(chr(ret))

out = out[:-2]

total = 0
for y in range(1, len(out)-2):
    for x in range(1, len(out[0])-2):
        try:
            if out[y][x] == "#" and out[y-1][x] == "#" and out[y+1][x] == "#" and out[y][x-1] == "#" and out[y][x+1] == "#":
                total += x * y
        except IndexError:
            print(y, x)
            raise IndexError

print(total)

y = len(out) - 1
for x in range(len(out[-1])-1):
    if out[-1][x] == "^":
        break

print(x, y)
dx = 0
dy = -1
mx = len(out[0]) - 1
my = len(out) - 1
steps = 0

visited = {(x, y)}
dirs = ""
while True:
    assert dx * dy == 0 and dx + dy != 0

    if 0 <= x+dx <= mx and 0 <= y+dy <= my and out[y+dy][x+dx] == "#":
        x += dx
        y += dy
        # visited.add((x, y))
        steps += 1
        continue

    if steps > 0:
        dirs += str(steps) + " "
        steps = 0

    if dx == 0:
        if 0 <= x+dy <= mx and out[y][x+dy] == "#":
            dirs += "L"
            dx = dy
            dy = 0
        else:
            try:
                assert out[y][x-dy] == "#"
            except:
                break
            dirs += "R"
            dx = -dy
            dy = 0
    else:
        assert dy == 0
        if 0 <= y-dx <= my and out[y-dx][x] == "#":
            dirs += "L"
            dy = -dx
            dx = 0
        else:
            assert out[y+dx][x] == "#"
            dirs += "R"
            dy = dx
            dx = 0

print(dirs)
abv = dirs.replace("L6", "a").replace("R12", "b").replace("L10", "c").replace("L4", "d").replace("L6", "e")
print(abv)
print(abv.replace("a a b a", "A").replace("c d a", "B"))
print(abv.replace("c d a", "B").replace("a b", "A"))
print(dirs.replace("L6 R12 L6 R12 L10 L4 L6", "A").replace("L6 R12 L6 L10 L10 L4 L6", "B").replace("R12 L10 L4 L6 L10 L10 L4 L6", "C"))
# print(dirs.replace("L6 R12", "A").replace("L10 L4", "B").replace("L6 L6", "C"))
inst = (
    "A,A,B,C,B\n"
    + "L,6,R,12,L,6,R,12,L,10,L,4,L,6\n"
    + "L,6,R,12,L,6,L,10,L,10,L,4,L,6\n"
    + "R,12,L,10,L,4,L,6,L,10,L,10,L,4,L,6\n"
)

intcode = Intcode("A", prog)
ret = intcode.run([ord(c) for c in inst])
print(list(map(len, inst.split())))
print(ret)

