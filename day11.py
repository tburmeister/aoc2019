import numpy as np

with open("day11.txt") as fp:
    raw = fp.read()

prog = list(map(int, raw.split(",")))


class Intcode:
    def __init__(self, name, prog):
        self.name = name
        self.prog = [0 for i in range(2**12)]
        for i, x in enumerate(prog):
            self.prog[i] = x
        self.pc = 0
        self.rb = 0

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
            self.prog[a] = x
        else:
            assert mode == 2
            self.prog[self.rb+a] = x
        
    def run(self, inputs):
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
                x = inputs[0]
                inputs = inputs[1:]
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

# 203 too low
intcode = Intcode("A", prog)
panel = np.zeros((100, 100))
seen = np.zeros((100, 100))
x = y = 50
panel[y][x] = 1
dx = 0
dy = -1

ret = -1
while ret is not None:
    val = panel[y][x]
    ret = intcode.run([val])
    if ret is None:
        break
    assert ret == 0 or ret == 1
    panel[y][x] = ret
    seen[y][x] = 1
    ret = intcode.run([])
    assert ret == 0 or ret == 1
    if ret == 0:
        if dx == 0: 
            dx, dy = dy, dx
        else:
            dx, dy = -dy, -dx
    else:
        if dx == 0:
            dx, dy = -dy, -dx
        else:
            dx, dy = dy, dx
    assert (dx + dy == 1 or dx + dy == -1) and dx * dy == 0

    x += dx
    y += dy

# 9938 too high
print(np.sum(seen))
print(x, y)
for row in panel:
    for col in row:
        print("#" if col else " ", end="")
    print()
        
