import numpy as np

with open("day16.txt") as fp:
    raw = fp.read().strip()

# raw = "80871224585914546619083218645595"
num = np.array([int(x) for x in raw])
num = np.array([int(x) for x in raw] * 10000)
s = len(num)

def mult(n, size):
    return np.round(np.sin(np.round(np.arange(n+1, size+1) // (n+1)) * np.pi * 0.5))

def multalt(mem, n, size):
    i = n
    mem[:i] = 0
    while i < size:
        mem[i:i+n+1] = 1
        mem[i+n+1:i+2*(n+1)] = 0
        mem[i+2*(n+1):i+3*(n+1)] = -1
        mem[i+3*(n+1):i+4*(n+1)] = 0
        i += 4*(n+1)

    return mem


for j in range(4):
    print(multalt(np.zeros(20), j, 20))

mem = np.zeros(s)
for i in range(100):
    print(i)
    new = np.zeros(s)
    for j in range(s):
        # print(mult(j, s-j))
        new[j] = np.abs(np.sum(multalt(mem, j, s) * num)) % 10

    num = new

# 43311147 too low
# print("".join(map(str, map(int, num[:8]))))
idx = int("".join(map(str, map(int, num[:7]))))
print("".join(map(str, map(int, num[idx:idx+8]))))

