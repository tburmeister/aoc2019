import re

class Planet:
    def __init__(self):
        self.parent = None
        self.children = []

    def sum(self):
        s = self.depth()
        for child in self.children:
            s += child.sum()

        return s

    def depth(self):
        if self.parent is None:
            return 0

        return self.parent.depth() + 1

    def depth_from(self, root):
        if self.parent is None:
            return 2**32

        if self.parent == root:
            return 0

        return self.parent.depth_from(root) + 1
        

regex = re.compile(r"(\w+)\)(\w+)")

with open("day6.txt") as fp:
    raw = fp.readlines()

ra = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".lstrip().split()
orbits = {}

for orb in raw:
    m = regex.match(orb)
    if m is None:
        raise Exception("can't match {}".format(orb))

    p, c = m.groups()
    if p not in orbits:
        orbits[p] = Planet()
    parent = orbits[p]
    if c not in orbits:
        orbits[c] = Planet()
    child = orbits[c]
    parent.children.append(child)
    child.parent = parent

com = orbits["COM"]
# for p in orbits.values():
#     print(p.parent)
# print(com.sum())
you = orbits["YOU"]
san = orbits["SAN"]

low = 2**32
for p in orbits.values():
    d1 = you.depth_from(p)
    d2 = san.depth_from(p)

    if d1 + d2 < low:
        low = d1 + d2

# 281 too low
# 279 too low
print(low)

