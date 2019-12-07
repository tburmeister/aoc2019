from itertools import permutations

with open("day7.txt") as fp:
    raw = fp.read()

prog = list(map(int, raw.split(",")))


class Intcode:
    def __init__(self, name, prog, source, phase):
        self.name = name
        self.prog = [x for x in prog]
        self.pc = 0
        self.source = source
        self.phase = phase
        self.inctr = 0
        
    def run(self, inputs):
        prog = self.prog
        pc = self.pc
        out = None

        while prog[pc] != 99:
            code = prog[pc]
            op = code % 100
            modes = [(code // 100) % 10, (code // 1000) % 10, (code // 10000) % 10]

            if op == 1:
                a, b, c = self.prog[pc+1:pc+4]
                prog[c] = (a if modes[0] else prog[a]) + (b if modes[1] else prog[b])
                pc += 4
            elif op == 2:
                a, b, c = prog[pc+1:pc+4]
                prog[c] = (a if modes[0] else prog[a]) * (b if modes[1] else prog[b])
                pc += 4
            elif op == 3:
                a = prog[pc+1]
                x = inputs[0]
                inputs = inputs[1:]
                print("{} received {}".format(self.name, x))
                prog[a] = x
                pc += 2
            elif op == 4:
                a = prog[pc+1]
                pc += 2
                out = a if modes[0] else prog[a]
                print("{} returning {}".format(self.name, out))
                break
            elif op == 5:
                a, b = prog[pc+1:pc+3]
                if (a if modes[0] else prog[a]) != 0:
                    pc = (b if modes[1] else prog[b])
                else:
                    pc += 3
            elif op == 6:
                a, b = prog[pc+1:pc+3]
                if (a if modes[0] else prog[a]) == 0:
                    pc = (b if modes[1] else prog[b])
                else:
                    pc += 3
            elif op == 7:
                a, b, c = prog[pc+1:pc+4]
                if (a if modes[0] else prog[a]) < (b if modes[1] else prog[b]):
                    prog[c] = 1
                else:
                    prog[c] = 0
                pc += 4
            elif op == 8:
                a, b, c = prog[pc+1:pc+4]
                if (a if modes[0] else prog[a]) == (b if modes[1] else prog[b]):
                    prog[c] = 1
                else:
                    prog[c] = 0
                pc += 4
            else:
                raise Exception("invalid opcode {}".format(op))

        self.prog = prog
        self.pc = pc
        return out


high = 0
for seq in permutations([5, 6, 7, 8, 9]):
    A = Intcode("A", prog, None, seq[0])
    B = Intcode("B", prog, A, seq[1])
    C = Intcode("C", prog, B, seq[2])
    D = Intcode("D", prog, C, seq[3])
    E = Intcode("E", prog, D, seq[4])

    ret = A.run([seq[0], 0])
    ret = B.run([seq[1], ret])
    ret = C.run([seq[2], ret])
    ret = D.run([seq[3], ret])
    ret = E.run([seq[4], ret])
    while ret is not None:
        out = ret
        ret = A.run([ret])
        ret = B.run([ret])
        ret = C.run([ret])
        ret = D.run([ret])
        ret = E.run([ret])

    print(out)
    if out > high:
        high = out

print(high)

