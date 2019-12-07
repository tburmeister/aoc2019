low = 108457
high = 562041
count = 0

for x in range(low, high+1):
    d1 = x % 10
    d2 = (x // 10) % 10
    d3 = (x // 100) % 10
    d4 = (x // 1000) % 10
    d5 = (x // 10000) % 10
    d6 = (x // 100000) % 10
    if not (d6 <= d5 <= d4 <= d3 <= d2 <= d1):
        continue
    if d1 == d2:
        if d2 != d3:
            print(x)
            count += 1
            continue
    if d2 == d3:
        if d3 != d4 and d1 != d2:
            print(x)
            count += 1
            continue
    if d3 == d4:
        if d4 != d5 and d2 != d3:
            print(x)
            count += 1
            continue
    if d4 == d5:
        if d5 != d6 and d3 != d4:
            print(x)
            count += 1
            continue
    if d5 == d6:
        if d4 != d5:
            print(x)
            count += 1

# 1708 too low
print(count)

