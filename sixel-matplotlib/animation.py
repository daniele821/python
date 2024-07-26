#!/bin/python3

import random
import matplotlib.pyplot as plt


x = []
y = []
plt.xlim(0, 10)
plt.ylim(0, 10)
for _ in range(10):
    x.append(random.randint(1, 5))
    y.append(random.randint(1, 5))
    plt.scatter(x, y)
    plt.pause(1)
