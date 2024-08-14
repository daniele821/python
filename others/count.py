# counting
count = 0
for i in range(701):
    if i % 2 == 0 or i % 5 == 0 or i % 7 == 0:
        count += 1
print(count)

# square sum
for i in range(1, 5):
    for j in range(1, 5):
        pass
        # print(i**2+j**2)

# dadi
for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            sorted = [a, b, c]
            sorted.sort(reverse=True)
            if sorted[0] >= 5 and sorted[1] >= 4 and sorted[2] >= 3:
                pass
                # print(sorted, a, b, c)
