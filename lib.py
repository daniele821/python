#!/bin/env python3


def solve(x):
    res = [x]
    while x > 1:
        if x % 2 == 0:
            x = x / 2
        else:
            x = x * 3 + 1
        res.append(int(x))
    return res


def plot_value(num):
    import matplotlib.pyplot as plt
    y = solve(num)
    x = range(len(y))
    plt.plot(x, y)
    plt.show()


def plot_range(start, end, map=lambda x: len(x)):
    if end < start:
        return
    import matplotlib.pyplot as plt
    x = range(start, end+1)
    y = [map(solve(x)) for x in range(start, end+1)]
    plt.plot(x, y)
    plt.show()
