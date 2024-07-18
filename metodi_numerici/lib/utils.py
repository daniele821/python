#!/bin/python3

import numpy as np


def load_mat(file):
    return np.load(
        "/personal/repos/daniele821/various_python/metodi_numerici/matrix/"
        + file + '.npy')


def load_all():
    A = [load_mat("A1"), load_mat("A2"), load_mat("A3"), load_mat("A4")]
    b = [load_mat("b1"), load_mat("b2"), load_mat("b3"), load_mat("b4")]
    return A, b
