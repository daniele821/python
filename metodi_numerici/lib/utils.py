#!/bin/python3

import numpy as np


def load_mat(file):
    return np.load(
        "/personal/repos/daniele821/various_python/metodi_numerici/matrix/"
        + file + '.npy')
