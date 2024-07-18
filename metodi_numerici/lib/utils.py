#!/bin/python3

from scipy.io import loadmat


def load_matlab(file, matrix):
    dati = loadmat(file)
    x = dati[matrix]
    x = x.astype(float)
    return x
