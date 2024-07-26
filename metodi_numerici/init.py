#!/bin/python3

from lib import utils, stats, checks, solve_triangular
import roots


def func(x): return x**4 - (13.5 * x**3) + (66 * x**2) - (138.5*x) + 105.5


error = 1e-2
roots.PAUSE = 0.8

_, _, bis1 = roots.bisection(func, 1.5, 2.5, error)
_, _, bis2 = roots.bisection(func, 2.5, 3.5, error)
_, _, bis3 = roots.bisection(func, 3.5, 4.5, error)
_, _, bis4 = roots.bisection(func, 4.5, 5.2, error)
roots.animate(func, bis1)
roots.animate(func, bis2)
roots.animate(func, bis3)
roots.animate(func, bis4)
