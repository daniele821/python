#!/bin/python3

from lib import utils, stats, checks, solve_triangular
import roots


def func(x): return x**4 - (13.5 * x**3) + (66 * x**2) - (138.5*x) + 105.5


x1, _, res1 = roots.bisection(func, 1.5, 2.5, 5e-2)
x2, _, res2 = roots.bisection(func, 2.5, 3.5, 5e-2)
x3, _, res3 = roots.bisection(func, 3.5, 4.5, 5e-3)
x4, _, res4 = roots.bisection(func, 4.5, 5.2, 5e-3)
print(res1, x1, func(x1))
print(res2, x2, func(x2))
print(res3, x3, func(x3))
print(res4, x4, func(x4))
roots.animate(func, res1, 0.5)
roots.animate(func, res2, 0.5)
roots.animate(func, res3, 0.5)
roots.animate(func, res4, 0.5)
