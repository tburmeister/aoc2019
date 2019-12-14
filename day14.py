import math
import re

regex = re.compile(r"(\d+) ([A-Z]+)")

with open("day14.txt") as fp:
    raw = fp.readlines()

if False:
    raw = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".strip().split("\n")

if False:
    raw = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""".strip().split("\n")

if False:
    raw = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".strip().split("\n")

if False:
    raw = """
1 ORE => 2 A
1 A => 1 B
1 A, 1 B => 1 FUEL""".strip().split("\n")

class Chem:
    def __init__(self, quantity, symbol):
        self.symbol = symbol
        self.quantity = quantity
        self.sources = []

    def __repr__(self):
        return "'{}' {}: {}".format(self.symbol, self.quantity, self.sources)

chems = {}
for react in raw:
    src, dst = react.split(" => ")
    q, s = regex.match(dst).groups()
    chem = Chem(int(q), s)
    chems[s] = chem
    for c in src.split(", "):
        q, s = regex.match(c).groups()
        chem.sources.append((int(q), s))

total = 0
gen = 0
resources = {s: 0 for s in chems.keys()}

while total < 1000000000000:
    to_gen = [(1, "FUEL")]
    ore = 0

    while len(to_gen) > 0:
        q, s = to_gen[0]
        to_gen = to_gen[1:]
        if s == "ORE":
            # print(q, "ORE")
            ore += q
            continue

        if q <= 0:
            # print(-q, s, "remainder")
            resources[s] -= q
            continue

        chem = chems[s]
        # print(q, s, chem.quantity, chems[s].sources, "have", resources[s])
        
        if q >= resources[s]:
            q -= resources[s]
            resources[s] = 0
        else:
            resources[s] -= q
            q = 0

        if q == 0:
            continue

        n = int(math.ceil(q / chem.quantity))
        r = n * chem.quantity - q
        to_gen = [(-r, s)] + to_gen
        for q, s in chem.sources[::-1]:
            # to_gen.append((q * n, s))
            to_gen = [(q * n, s)] + to_gen

    total += ore
    gen += 1
    if (total // 1000000000) % 10 == 0:
        print(gen, total)

# 392026 too high
# 277946 too low
print(resources)
print(ore)

