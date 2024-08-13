# counting
count = 0
for i in range(1, 101):
    if i % 2 == 0 or i % 3 == 0 or i % 5 == 0:
        count += 1

# square sum
for i in range(1, 5):
    for j in range(1, 5):
        print(i**2+j**2)
