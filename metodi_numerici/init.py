#!/bin/python3

from lib import utils, stats, checks, solve_triangular
import roots


def func(x): return x**4 - (13.5 * x**3) + (66 * x**2) - (138.5*x) + 105.5
def corm(func, a, b): return (func(b) - func(a)) / (b - a)


error = 1e-3
itmax = 20
bisopts = ['vert']
falopts = ['vert', 'falsi']
coropts = ['vert']


_, _, bis1 = roots.bisection(func, 1.5, 2.5, error)
_, _, bis2 = roots.bisection(func, 2.5, 3.5, error)
_, _, bis3 = roots.bisection(func, 3.5, 4.5, error)
_, _, bis4 = roots.bisection(func, 4.5, 5.2, error)
_, _, fal1 = roots.falsi(func, 1.5, 2.5, error, error, itmax)
_, _, fal2 = roots.falsi(func, 2.5, 3.5, error, error, itmax)
_, _, fal3 = roots.falsi(func, 3.5, 4.5, error, error, itmax)
_, _, fal4 = roots.falsi(func, 4.5, 5.2, error, error, itmax)
x1, it1, cor1 = roots.corde(func, corm(func, 1.5, 2.5), 1.5, error, error, itmax)
x2, it2, cor2 = roots.corde(func, corm(func, 2.5, 3.5), 2.5, error, error, itmax)
x3, it3, cor3 = roots.corde(func, corm(func, 3.5, 4.5), 3.5, error, error, itmax)
x4, it4, cor4 = roots.corde(func, corm(func, 4.5, 5.2), 4.5, error, error, itmax)
print(x1, x2, x3, x4)
print(it1, it2, it3, it4)
# roots.animate(func, bis1, 1.5, 2.5, bisopts)
# roots.animate(func, bis2, 2.5, 3.5, bisopts)
# roots.animate(func, bis3, 3.5, 4.5, bisopts)
# roots.animate(func, bis4, 4.5, 5.2, bisopts)
# roots.animate(func, fal1, 1.5, 2.5, falopts)
# roots.animate(func, fal2, 2.5, 3.5, falopts)
# roots.animate(func, fal3, 3.5, 4.5, falopts)
# roots.animate(func, fal4, 4.5, 5.2, falopts)
roots.animate(func, cor1, 1.5, 2.5, coropts)
roots.animate(func, cor2, 2.5, 3.5, coropts)
roots.animate(func, cor3, 3.5, 4.5, coropts)
roots.animate(func, cor4, 4.5, 5.2, coropts)
