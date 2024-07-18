#!/bin/python3

import numpy as np


def is_symmetrical(A):
    return (A.T == A).all()


def is_positive_definite(A):
    return np.all(np.linalg.eigvals(A) > 0)


def is_diagonally_dominant(A):
    diag = np.abs(np.diag(A))
    rest = np.abs(A.copy())
    np.fill_diagonal(rest, 0)
    sums = np.sum(rest, axis=1)
    return (diag > sums).all()


if __name__ == "__main__":
    size = 500
    A = np.random.rand(size, size)
    A1 = A.copy()
    np.fill_diagonal(A1, np.sum(np.abs(A), axis=1))
    assert is_symmetrical(A@A.T)
    assert is_positive_definite(A@A.T)
    assert is_diagonally_dominant(A1)
