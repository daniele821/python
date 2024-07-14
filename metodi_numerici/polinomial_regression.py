#!/bin/python3


import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('module://matplotlib-backend-sixel')


def regression(X, Y, order=None):
    B = np.vander(X, order or len(X), increasing=True)
    BT = B.T.copy()
    coeff = np.linalg.solve(BT@B, BT@Y)

    # draw
    plt.plot(X, Y, 's')
    X1 = np.linspace(np.min(X), np.max(X), 100)
    Y1 = np.polyval(np.flip(coeff), X1)
    plt.plot(X1, Y1)
    plt.show()

    return coeff


X = [0, 0.3, 0.8, 1.1, 1.6, 2.3]
Y = [0.5, 0.82, 1.14, 1.25, 1.35, 1.4]
print(regression(X, Y, 2))
print(regression(X, Y, 3))
