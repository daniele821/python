#!/bin/python3

from lib import utils, stats, checks, solve_triangular
import roots


def func(x): return x**4 - (13.5 * x**3) + (66 * x**2) - (138.5*x) + 105.5


_, _, vecx = roots.bisection(func, 1.5, 2.5, 1e-12)
print(vecx)
