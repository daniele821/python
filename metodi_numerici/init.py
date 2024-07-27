#!/bin/python3

from lib import utils, stats, checks, solve_triangular
import roots


def func(x): return x**4 - (13.5 * x**3) + (66 * x**2) - (138.5*x) + 105.5


error = 1e-2
itmax = 1000
bisopts = ['vert', 'points']
falopts = ['vert', 'points', 'falsi']


_, _, bis1 = roots.bisection(func, 1.5, 2.5, error)
_, _, bis2 = roots.bisection(func, 2.5, 3.5, error)
_, _, bis3 = roots.bisection(func, 3.5, 4.5, error)
_, _, bis4 = roots.bisection(func, 4.5, 5.2, error)
_, _, fal1 = roots.falsi(func, 1.5, 2.5, error, error, itmax)
_, _, fal2 = roots.falsi(func, 2.5, 3.5, error, error, itmax)
_, _, fal3 = roots.falsi(func, 3.5, 4.5, error, error, itmax)
_, _, fal4 = roots.falsi(func, 4.5, 5.2, error, error, itmax)
roots.PAUSE = 0.5
roots.DRAWALL = False
roots.animate(func, bis1, 1.5, 2.5, bisopts)
roots.animate(func, bis2, 2.5, 3.5, bisopts)
roots.animate(func, bis3, 3.5, 4.5, bisopts)
roots.animate(func, bis4, 4.5, 5.2, bisopts)
roots.PAUSE = 0.5
roots.DRAWALL = True
roots.animate(func, fal1, 1.5, 2.5, falopts)
roots.animate(func, fal2, 2.5, 3.5, falopts)
roots.animate(func, fal3, 3.5, 4.5, falopts)
roots.animate(func, fal4, 4.5, 5.2, falopts)
