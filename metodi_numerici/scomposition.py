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
    print("jacobi spectral radius: ", np.max(np.linalg.eigvals(T)))
    if np.max(np.linalg.eigvals(T)) >= 1:
        raise ValueError("Jacobbi cannot converge")

    # iterate toward the solution
    while it < itmax and error > toll:
        x = T@x0 + invM@b
        error = np.linalg.norm(x - x0) / (np.linalg.norm(x))
        x0 = x.copy()
        it += 1

    return x, it


def gauss_seidel(A, b, x0, toll, itmax):
    D = np.diag(np.diag(A))
    E = np.tril(A, -1)
    F = np.triu(A, 1)
    M = D + E
    invM = np.linalg.inv(M)
    N = -F
    T = invM @ N
    it = 1
    error = np.inf

    # check for convergence
    print("gauss_seidel spectral radius: ", np.max(np.linalg.eigvals(T)))
    if (np.max(np.linalg.eigvals(T)) >= 1):
        raise ValueError("Gauss-seidel cannot converge")

    # iterate toward the solution
    while it < itmax and error > toll:
        x, _ = solve_triangular.Lsolve(M, N@x0+b)
        error = np.linalg.norm(x-x0) / np.linalg.norm(x)
        x0 = x.copy()
        it += 1

    return x, it


def gauss_seidel_acc(A, b, x0, toll, itmax, omega):
    raise Exception("Todo")


if __name__ == '__main__':
    A, b = utils.load_all()
    inf = np.inf
    # checks
    assert checks.is_diagonally_dominant(A[2])
    assert checks.is_symmetrical(A[2]) and checks.is_positive_definite(A[2])
    assert checks.is_symmetrical(A[3]) and checks.is_positive_definite(A[3])
    # jacobi
    _, _ = jacobi(A[2], b[2], np.zeros_like(b[2]), 1e-15, inf)
    # gauss-seidel
    _, _ = gauss_seidel(A[2], b[2], np.zeros_like(b[2]), 1e-10, inf)
    _, _ = gauss_seidel(A[3], b[3], np.zeros_like(b[3]), 1e-4, inf)
    # gauss-seidel accelerated
    _, _ = gauss_seidel_acc(A[2], b[2], np.zeros_like(b[2]), 1e-10, inf, 1.67)
    _, _ = gauss_seidel_acc(A[3], b[3], np.zeros_like(b[3]), 1e-4, inf, 1.33)
