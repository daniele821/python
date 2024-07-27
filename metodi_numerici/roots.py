#!/bin/python3

import numpy as np
import math
import matplotlib.pyplot as plt


PAUSE = 1


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


def animate(func, vecx):
    a = min(vecx)
    b = max(vecx)
    fa = func(a)
    fb = func(b)
    for i in range(len(vecx) - 1):
        plt.clf()
        X = np.linspace(a, b, 100)
        Y = func(X)
        plt.grid(True)
        plt.plot(X, Y, 'r')
        X = np.linspace(a, b, 100)
        Y = np.zeros_like(X)
        plt.plot(X, Y, 'k')
        for xk in vecx[:i+1]:
            plt.plot([xk, xk], [fa, fb], 'k--.')
        x = [vecx[i], vecx[i+1]]
        y = [0, func(vecx[i+1])]
        plt.plot(x, y, 'g')
        plt.scatter(x, y)
        plt.scatter(vecx[:i], np.zeros((i)))
        plt.pause(PAUSE)
    plt.show()
