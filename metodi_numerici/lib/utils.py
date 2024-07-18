#!/bin/python3

import numpy as np


def load_mat(file):
    return np.load(
        "/personal/repos/daniele821/various_python/metodi_numerici/matrix/"
        + file + '.npy')


def load_all():
    A = [load_mat("A" + str(x+1)) for x in range(4)]
    b = [load_mat("b" + str(x+1)) for x in range(4)]
    return A, b
