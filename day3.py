with open("day3.txt") as fp:
    raw1, raw2 = fp.readlines()

w1 = raw1.split(",")
w2 = raw2.split(",")

def trace(w):
    x, y = 0, 0
    path = set()
    steps = {}
    s = 0
    for d in w:
        if d[0] == "R":
            for i in range(int(d[1:])):
                x += 1
                s += 1
                path.add((x, y))
                steps[(x, y)] = s
        elif d[0] == "L":
            for i in range(int(d[1:])):
                x -= 1
                s += 1
                path.add((x, y))
                steps[(x, y)] = s
        elif d[0] == "U":
            for i in range(int(d[1:])):
                y += 1
                s += 1
                path.add((x, y))
                steps[(x, y)] = s
        else:
            assert d[0] == "D"
            for i in range(int(d[1:])):
                y -= 1
                s += 1
                path.add((x, y))
                steps[(x, y)] = s

    return path, steps

path1, steps1 = trace(w1)
path2, steps2 = trace(w2)
ints = path1.intersection(path2)
low = 2**32
best = None
for x, y in ints:
    d = steps1[(x, y)] + steps2[(x, y)]
    if d < low:
        low = d
        best = (x, y)

print(ints)
print(low)

