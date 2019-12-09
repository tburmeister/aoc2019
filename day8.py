import numpy as np

with open("day8.txt") as fp:
    raw = fp.read().strip()

img = np.array([int(d) for d in raw])
w = 25
h = 6
l = len(img) // (h * w)

img = img.reshape((l, h, w))
low = 2**32
best = None
for layer in img:
   zeros = np.sum(layer == 0)
   if zeros < low:
       low = zeros
       best = layer

# print(np.sum(best == 1) * np.sum(best == 2))

def show(out):
    for row in out:
        for col in row:
            print(u"\u2588" if int(col) == 1 else " ", end="")
        print()

out = np.zeros((h, w)) + 2
for layer in img[::1]:
    out[out == 2] = layer[out == 2]

show(out)

