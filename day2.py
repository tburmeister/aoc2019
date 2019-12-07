with open("day2.txt") as fp:
    raw = fp.read()

# raw = "1,1,1,4,99,5,6,0,99"
prog = list(map(int, raw.split(",")))

def run(prog):
    prog = [x for x in prog]
    pc = 0
    while prog[pc] != 99:
        op, a, b, c = prog[pc:pc+4]

        if op == 1:
            prog[c] = prog[a] + prog[b]
        elif op == 2:
            prog[c] = prog[a] * prog[b]
        else:
            raise Exception("invalid opcode {}".format(op))

        pc += 4

    return prog[0]

def main():
    for n in range(100):
        prog[1] = n
        for v in range(100):
            prog[2] = v
            print(n, v)
            try:
                r = run(prog)
                if r == 19690720:
                    return 100 * n + v
            except:
                continue

print(main())

