#!/bin/python3

import numpy as np


def is_symmetrical(A):
    if (len(A.shape) != 2) or (A.shape[0] != A.shape[1]):
        return False
    return (A.T == A).all()


def is_positive_definite(A):
    if not is_symmetrical(A):
        return False
    for i in range(1, A.shape[1] + 1):
        submatrix = A[:i, :i]
        if np.linalg.det(submatrix) < 0:
            return False
    return True


if __name__ == "__main__":
    A = np.array([[1.0, 2.0, 3.0], [2.0, 5.0, 4.0], [3.0, 4.0, 6.0]])
    assert is_symmetrical(A), "symmetrical check fails"
    assert is_positive_definite(A@A.T), "positive_definite check fails"
