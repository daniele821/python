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


def falsi(func, a, b, tolx, tolf, itmax):
    fa = func(a)
    fb = func(b)
    fx = np.inf
    if sign(fa) * sign(fb) >= 0:
        raise ValueError('cannot apply falsi')
    it = 0
    vecx = []

    while abs(b - a) > tolx and abs(fx) >= tolf and it < itmax:
        x = a - fa * (b - a) / (fb - fa)
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


def animate(func, vecx, a, b, opts=['vert', 'falsi', 'corde']):
    # extremes of the graph
    A = a
    B = b
    FA = func(a)
    FB = func(b)
    fa = FA
    fb = FB
    fx1 = np.linspace(a, b, 100)
    fy1 = func(fx1)
    fx2 = np.copy(fx1)
    fy2 = np.zeros_like(fx2)
    all = []

    for i in range(len(vecx)):
        plt.clf()
        plt.grid(True)

        # draw function in study
        plt.plot(fx1, fy1, 'r')

        # draw x axis line
        plt.plot(fx2, fy2, 'k')

        # draw y axis of iterative solutions
        if 'vert' in opts:
            plt.plot([A, A], [FB, FA], 'k--.')
            plt.plot([B, B], [FB, FA], 'k--.')
            for xk in vecx[:i]:
                plt.plot([xk, xk], [FB, FA], 'k--.')
            plt.plot([a, a], [FB, FA], 'y-')
            plt.plot([b, b], [FB, FA], 'y-')

        # falsi lines
        if 'falsi' in opts:
            for elem in all:
                plt.plot(elem[0], elem[1], 'b')
            plt.plot([a, b], [fa, fb], 'b')

        # calculations
        all.append([[a, b], [fa, fb]])
        x = vecx[i]
        y = func(x)
        if sign(y) * sign(fa) > 0:
            fa = y
            a = x
        elif sign(y) * sign(fb) > 0:
            fb = y
            b = x

        # make animation
        plt.pause(PAUSE)
    plt.show()
