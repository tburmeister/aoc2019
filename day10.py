import math

from itertools import combinations

with open("day10.txt") as fp:
    raw = fp.readlines()

r = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".strip().split()

asts = []
for y, row in enumerate(raw):
    for x, col in enumerate(row):
        if col == "#":
            asts.append((x, y))

def line(x1, y1, x2, y2):
    if x1 == x2:
        return None, x1
    m = float(y2 - y1) / float(x2 - x1)
    b = y1 - m * x1
    return round(m, 5), round(b, 5)

lines = {}
for (x1, y1), (x2, y2) in combinations(asts, 2):
    l = line(x1, y1, x2, y2)
    if l not in lines:
        lines[l] = set()
    lines[l].add((x1, y1))
    lines[l].add((x2, y2))


out = {}
for l, pts in lines.items():
    for i, pt in enumerate(sorted(pts, reverse=(l[0] is not None and l[0] > 0))):
        if pt not in out:
            out[pt] = 0
        if i == 0 or i == (len(pts) - 1):
            out[pt] += 1
        else:
            out[pt] += 2

high = 0
best = None
for pt, cnt in out.items():
    if cnt > high:
        best = pt
        high = cnt

# 277 too low
print(high)
print(best)


class Cmp:
    def cmp(self, pt):
        pass

    def __lt__(self, pt):
        return self.cmp(pt) < 0

    def __gt__(self, pt):
        return self.cmp(pt) > 0

    def __eq__(self, pt):
        return self.cmp(pt) == 0

    def __le__(self, pt):
        return self.cmp(pt) <= 0

    def __ge__(self, pt):
        return self.cmp(pt) >= 0

    def __ne__(self, pt):
        return self.cmp(pt) != 0

class Point(Cmp):
    bx, by = best
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def dist(self):
        return math.sqrt((self.x - self.bx)**2 + (self.y - self.by)**2)

    def cmp(self, pt):
        d1 = self.dist()
        d2 = pt.dist()
        if d1 < d2:
            return -1
        if d1 > d2:
            return 1
        return 0

class Line(Cmp):
    def __init__(self, m, quad, pts):
        if m is None:
            self.m = -10000000
        else:
            self.m = m 
        self.quad = quad
        self.pts = sorted([Point(*pt) for pt in pts])

    def __repr__(self):
        return str(self.quad) + ":" + str(self.m) + ":" + repr(self.pts)

    def cmp(self, line):
        if self.quad < line.quad:
            return -1
        if self.quad > line.quad:
            return 1
        if self.m < line.m:
            return -1
        if self.m > line.m:
            return 1
        return 0

vap = set()
vecs = []
for (m, b), pts in lines.items():
    if best in pts:
        sp = sorted(pts, reverse=(l[0] is not None and l[0] > 0))
        vap.update(pts)
        idx = sp.index(best)
        if m is None:
            vecs.append(Line(m, 0, sp[:idx]))
            vecs.append(Line(m, 2, sp[idx+1:]))
        elif m < 0:
            vecs.append(Line(m, 2, sp[:idx]))
            vecs.append(Line(m, 0, sp[idx+1:]))
        elif m >= 0:
            vecs.append(Line(m, 3, sp[:idx]))
            vecs.append(Line(m, 1, sp[idx+1:]))

vecs = sorted([v for v in vecs if len(v.pts) > 0])
for v in vecs:
    print(v)
count = 0
while count < 200:
    for vec in vecs:
        if len(vec.pts) == 0:
            continue
        first = vec.pts[0]
        vec.pts = vec.pts[1:]
        count += 1
        if count == 200:
            break
        print(first, count)

print(first)

# 1706 too high
# 1503 too high
# 318 too low
# 1008?

