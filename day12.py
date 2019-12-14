import numpy as np
from itertools import combinations

"""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
sample = np.array([
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1]
])

pos = np.array([
    [14, 15, -2],
    [17, -3, 4],
    [6, 12, -13],
    [-2, 10, -8]
], dtype=np.int)
vel = np.zeros((4, 3), dtype=np.int)
pairs = list(combinations(range(4), 2))
iters = 1000

# pos = sample
# iters = 10

"""
seen = {hash(str(vel))}
for k in range(iters):
    for i, j in pairs:
        mask = pos[i] < pos[j]
        vel[i][mask] += 1
        vel[j][mask] -= 1
        mask = pos[i] > pos[j]
        vel[i][mask] -= 1
        vel[j][mask] += 1

    pos += vel
"""
iters = 10000000000
print(pos)
print(vel)

for j in range(3):
    for k in range(iters):
        for i in range(4):
            vel[i, j] -= np.sum(pos[:, j] < pos[i, j])
            vel[i, j] += np.sum(pos[:, j] > pos[i, j])

        pos[:, j] += vel[:, j]

        if np.all(vel[:, j] == 0):
            print(k + 1)
            break

# 2x ouput
# 288289680000 too high
# 40916 too high
print(np.sum(np.sum(np.abs(pos), 1) * np.sum(np.abs(vel), 1)))

