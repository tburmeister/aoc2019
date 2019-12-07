import numpy as np

with open("day1.txt") as fp:
    raw = fp.readlines()

data = []
for row in raw:
    data.append(int(row))

data = np.array(data)

total = data // 3 - 2
add = np.maximum(total // 3 - 2, 0)
while np.any(add > 0):
    total += add
    add = np.maximum(add // 3 - 2, 0)

print(np.sum(total))

