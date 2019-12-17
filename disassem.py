with open("day17.txt") as fp:
    raw = fp.read()

prog = list(map(int, raw.split(",")))


class Intcode:
    def __init__(self, name, prog):
        self.name = name
        self.prog = prog + [0, 0, 0]

    def decode(self):
        prog = self.prog
        pc = 0
        out = ""

        while pc < len(prog) - 3:
            code = prog[pc]
            op = code % 100
            modes = [(code // 100) % 10, (code // 1000) % 10, (code // 10000) % 10]
            a, b, c = prog[pc+1:pc+4]
            m = []
            for mode in modes:
                if mode == 0:
                    m.append("a")
                if mode == 1:
                    m.append("i")
                else:
                    m.append("r")

            if 0 < op <= 9 or op == 99:
                out += "{}\t".format(pc)

            if op == 1:
                out += "ADD {}({}) {}({}) {}({})\n".format(m[0], a, m[1], b, m[2], c)
                pc += 4
            elif op == 2:
                out += "MUL {}({}) {}({}) {}({})\n".format(m[0], a, m[1], b, m[2], c)
                pc += 4
            elif op == 3:
                out += "INP {}({})\n".format(m[0], a)
                pc += 2
            elif op == 4:
                out += "OUT {}({})\n".format(m[0], a)
                pc += 2
            elif op == 5:
                out += "BNZ {}({}) {}({})\n".format(m[0], a, m[1], b)
                pc += 3
            elif op == 6:
                out += "BEZ {}({}) {}({})\n".format(m[0], a, m[1], b)
                pc += 3
            elif op == 7:
                out += "SLT {}({}) {}({}) {}({})\n".format(m[0], a, m[1], b, m[2], c)
                pc += 4
            elif op == 8:
                out += "SEQ {}({}) {}({}) {}({})\n".format(m[0], a, m[1], b, m[2], c)
                pc += 4
            elif op == 9:
                out += "RBI {}({})\n".format(m[0], a)
                pc += 2
            elif op == 99:
                out += "END\n"
                pc += 1
            else:
                pc += 1

        return out

prog[0] = 2
intcode = Intcode("A", prog)
print(intcode.decode())
      
