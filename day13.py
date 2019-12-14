import numpy as np

with open("day13.txt") as fp:
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
        
    def run(self, input_func):
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
                # x = inputs[0]
                # inputs = inputs[1:]
                x = input_func()
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

prog[0] = 2
print(prog[369])
prog[369] = 1105
input()
intcode = Intcode("A", prog)
panel = np.zeros((23, 42), dtype=np.int)
x = y = 0

def input_func():
    for row in panel:
        for col in row:
            print(col, end="")
        print()
    # return int(input("control: "))
    return 0

ret = -1
while ret is not None:
    val = panel[y][x]
    x = intcode.run(input_func)
    if x is None:
        break

    y = intcode.run(input_func)
    assert y is not None
    v = intcode.run(input_func)
    if x == -1:
        print("score:", v)
    else:
        assert 0 <= v <= 4
        panel[y][x] = v

print(np.sum(panel == 2))
       
