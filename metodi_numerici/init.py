#!/bin/python3

from lib import utils, stats, checks, solve_triangular
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('module://matplotlib-backend-sixel')


def spectral_radius(T):
    spectral_radius = np.max(np.linalg.eigvals(T))
    return spectral_radius


def omega_matrix(D, E, F, w):
    T = np.linalg.inv(D + w * E) @ ((1 - w) * D - w * F)
    return T


def omega_spectral_radius(D, E, F, w):
    return spectral_radius(omega_matrix(D, E, F, w))


A, b = utils.load_all()
A = A[3]
D = np.diag(np.diag(A))
E = np.tril(A, -1)
F = np.triu(A, 1)
Tj = np.linalg.inv(D)@(-E-F)
Tg = np.linalg.inv(D+E)@(-F)

spectral_radius(Tj)
spectral_radius(Tg)

X = np.linspace(1.30, 1.35, 50)
Y = np.array([omega_spectral_radius(D, E, F, w) for w in X])
plt.plot(X, Y, 's')
plt.show()
print(np.min(Y))
