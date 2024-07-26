#!/bin/python3

import numpy as np
import math
import matplotlib.pyplot as plt


def sign(x):
    return math.copysign(1, x)


def bisection(func, a, b, tolx):
    fa = func(a)
    fb = func(b)
    if sign(fa) * sign(fb) >= 0:
        raise ValueError('cannot apply bisection')
    it = 0
    vecx = []

    while abs(b - a) > tolx:
        x = a + (b - a) / 2
        vecx.append(x)
        fx = func(x)
        it += 1

        if abs(fx) <= np.spacing(1):
            break

        if sign(fa) * sign(fx) > 0:
            fa = fx
            a = x
        elif sign(fx) * sign(fb) > 0:
            fb = fx
            b = x

    return x, it, vecx


# def animate(func, vecx, pause):
#     a = min(vecx) - 1
#     b = max(vecx) + 1
#     fa = func(a)
#     fb = func(b)
#     plt.xlim(a, b)
#     plt.xlim(fa, fb)
#     X = np.linspace(a, b, 200)
#     Y = func(X)
#     plt.plot(X, Y)
#     for i in range(len(vecx) - 1):
#         plt.xlim(a, b)
#         plt.xlim(fa, fb)
#         X = np.linspace(a, b, 200)
#         Y = func(X)
#         plt.plot(X, Y)
#         plt.pause(pause)
