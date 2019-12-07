with open("day5.txt") as fp:
    raw = fp.read()

# raw = "1,1,1,4,99,5,6,0,99"
# raw = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
prog = list(map(int, raw.split(",")))

def run(prog):
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
            x = int(input("IN: "))
            a = prog[pc+1]
            prog[a] = x
            pc += 2
        elif op == 4:
            a = prog[pc+1]
            print("OUT: ", (a if modes[0] else prog[a]))
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

run(prog)

