#!/bin/python3

import numpy as np
import math
import matplotlib.pyplot as plt


PAUSE = 0.8


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
        m = (fb - fa) / (b - a)
        x = a - fa / m
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


def corde(func, m, x0, tolx, tolf, itmax):
    it = 0
    vecx = []

    while True:
        x1 = x0 - func(x0) / m
        vecx.append(x1)
        it += 1

        if it >= itmax or abs(func(x1)) <= tolf or abs(x1-x0)/abs(x1) <= tolx:
            break

        x0 = x1

    return x1, it, vecx


def newton(func, dfunc, x0, tolx, tolf, itmax):
    it = 0
    vecx = []

    while True:
        if abs(dfunc(x0)) <= np.spacing(1):
            raise ValueError('Newton method failed: derivate is zero')

        x1 = x0 - func(x0) / dfunc(x0)
        vecx.append(x1)
        it += 1

        if it >= itmax or abs(func(x1)) <= tolf or abs(x1-x0)/abs(x1) <= tolx:
            break

        x0 = x1

    return x1, it, vecx


def animate(func, vecx, a, b, x0=None, opts=['vert', 'falsi', 'corde']):
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
    falsi = []
    corde = []

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
            for elem in falsi:
                plt.plot(elem[0], elem[1], 'b')
            plt.plot([a, b], [fa, fb], 'b')

        # corde lines
        if 'corde' in opts:
            x = vecx[i]
            y = func(x)
            xold = vecx[i-1]
            yold = func(xold)
            if i == 0:
                xold = x0
                yold = func(x0)
            corde.append([[x, xold], [0, yold]])
            for elem in corde:
                plt.plot(elem[0], elem[1], 'b')

        # calculations
        falsi.append([[a, b], [fa, fb]])
        x = vecx[i]
        y = func(x)
        if sign(y) * sign(fa) > 0:
            fa = y
            a = x
        elif sign(y) * sign(fb) > 0:
            fb = y
            b = x

        # add legends
        plt.legend([f"{i+1} / {len(vecx)}"])

        # make animation
        plt.pause(PAUSE)
    plt.show()


if __name__ == '__main__':
    def func(x): return x**4 - (13.5 * x**3) + (66 * x**2) - (138.5*x) + 105.5
    def dfunc(x): return (4 * x**3) - (41.5 * x**2) + (132 * x) - 138.5
    def corm(func, a, b): return (func(b) - func(a)) / (b - a)

    error = 1e-3
    itmax = 20
    bisopts = ['vert']
    falopts = ['vert', 'falsi']
    coropts = ['vert', 'corde']

    def anim(name, vecx, a, b, x0, opts):
        print(f"animation {name}")
        try:
            animate(func, vecx, a, b, x0, opts)
        except KeyboardInterrupt:
            print("skipping animation...")

    _, _, bis1 = bisection(func, 1.5, 2.5, error)
    _, _, bis2 = bisection(func, 2.5, 3.5, error)
    _, _, bis3 = bisection(func, 3.5, 4.5, error)
    _, _, bis4 = bisection(func, 4.5, 5.2, error)
    _, _, fal1 = falsi(func, 1.5, 2.5, error, error, itmax)
    _, _, fal2 = falsi(func, 2.5, 3.5, error, error, itmax)
    _, _, fal3 = falsi(func, 3.5, 4.5, error, error, itmax)
    _, _, fal4 = falsi(func, 4.5, 5.2, error, error, itmax)
    _, _, cor1 = corde(func, corm(func, 1.5, 2.5), 1.5, error, error, itmax)
    _, _, cor2 = corde(func, corm(func, 2.5, 3.5), 2.5, error, error, itmax)
    _, _, cor3 = corde(func, corm(func, 3.5, 4.5), 3.5, error, error, itmax)
    _, _, cor4 = corde(func, corm(func, 4.5, 5.2), 4.5, error, error, itmax)
    _, _, new1 = newton(func, dfunc, 1.5, error, error, itmax)
    _, _, new2 = newton(func, dfunc, 2.5, error, error, itmax)
    _, _, new3 = newton(func, dfunc, 3.5, error, error, itmax)
    _, _, new4 = newton(func, dfunc, 4.5, error, error, itmax)
    anim('bisection 1', bis1, 1.5, 2.5, None, bisopts)
    anim('bisection 2', bis2, 2.5, 3.5, None, bisopts)
    anim('bisection 3', bis3, 3.5, 4.5, None, bisopts)
    anim('bisection 4', bis4, 4.5, 5.2, None, bisopts)
    anim('falsi 1', fal1, 1.5, 2.5, None, falopts)
    anim('falsi 2', fal2, 2.5, 3.5, None, falopts)
    anim('falsi 3', fal3, 3.5, 4.5, None, falopts)
    anim('falsi 4', fal4, 4.5, 5.2, None, falopts)
    anim('corde 1', cor1, 1.5, 2.5, 2.5, coropts)
    anim('corde 2', cor2, 2.5, 3.5, 2.5, coropts)
    anim('corde 3', cor3, 3.5, 4.5, 3.5, coropts)
    anim('corde 4', cor4, 4.5, 5.2, 4.5, coropts)
    anim('newton 1', new1, 1.5, 2.5, 2.5, coropts)
    anim('newton 2', new2, 2.5, 3.5, 3.5, coropts)
    anim('newton 3', new3, 3.5, 4.5, 4.5, coropts)
    anim('newton 4', new4, 4.5, 5.2, 5.2, coropts)
