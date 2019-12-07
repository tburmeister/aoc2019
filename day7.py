from itertools import permutations

with open("day7.txt") as fp:
    raw = fp.read()

prog = list(map(int, raw.split(",")))


def run(prog, inputs, outputs):
    prog = [x for x in prog]
    pc = 0
    while prog[pc] != 99:
        code = prog[pc]
        op = code % 100
        modes = [(code // 100) % 10, (code // 1000) % 10, (code // 10000) % 10]

        if op == 1:
            a, b, c = prog[pc+1:pc+4]
            prog[c] = (a if modes[0] else prog[a]) + (b if modes[1] else prog[b])
            pc += 4
        elif op == 2:
            a, b, c = prog[pc+1:pc+4]
            prog[c] = (a if modes[0] else prog[a]) * (b if modes[1] else prog[b])
            pc += 4
        elif op == 3:
            x = inputs[0]
            inputs = inputs[1:]
            a = prog[pc+1]
            prog[a] = x
            pc += 2
        elif op == 4:
            a = prog[pc+1]
            outputs.append(a if modes[0] else prog[a])
            pc += 2
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

    return prog[0]

high = 0
for seq in permutations([0, 1, 2, 3, 4]):
    out = [0]
    for i in range(5):
        run(prog, [seq[i], out[-1]], out)

    print(out)
    if out[-1] > high:
        high = out[-1]

# 90690 too low
print(high)


