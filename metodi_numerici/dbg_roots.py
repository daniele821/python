#!/bin/python3

import numpy as np
import math


def sign(x):
    return math.copysign(1, x)


def bisection(func, a, b, tolx):
    fa = func(a)
    fb = func(b)
    if sign(fa) * sign(fb) >= 0:
        raise ValueError('cannot apply bisection')
    it = 0

    while math.abs(b - a) > tolx:
        x = a + (b - a) / 2
        fx = func(x)

        if fx <= np.spacing(1):
            return x

        if sign(fa) * sign(fx) > 0:
            fa = fx
            a = x
        elif sign(fx) * sign(fb) > 0:
            fb = fx
            b = x

        it += 1

    return x, it
