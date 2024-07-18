#!/bin/python3

import numpy as np
from lib import utils, stats, checks, solve_triangular


def jacobi(A, b, x0, toll, itmax):
    D = np.diag(np.diag(A))
    E = np.tril(A, -1)
    F = np.triu(A, 1)
    M = D
    invM = np.linalg.inv(M)
    N = -(E+F)
    T = invM@N
    error = np.inf
    it = 1

    # check for convergence
    if np.max(np.linalg.eigvals(T)) >= 1:
        raise ("Jacobbi cannot converge")

    # iterate to the solution
    while it < itmax and error > toll:
        x = T@x0 + invM@b
        error = np.linalg.norm(x - x0) / (np.linalg.norm(x))
        x0 = x.copy()
        it += 1

    return x, it


if __name__ == '__main__':
    A, b = utils.load_all()
    # checks
    assert checks.is_diagonally_dominant(A[2])
    # jacobi
    _, _ = jacobi(A[2], b[2], np.zeros_like(b[2]), 1e-16, np.inf)
