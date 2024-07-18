#!/bin/python3

import numpy as np


def is_symmetrical(A):
    if (len(A.shape) != 2):
        raise ValueError('array not a 2D matrix')
    return (A.T == A).all()


def is_positive_definite(A):
    return


if __name__ == "__main__":
    A = np.array([[1.0, 2.0, 3.0], [2.0, 5.0, 4.0], [3.0, 4.0, 6.0]])
    print(is_symmetrical(A))
