#!/bin/python3

import scipy
import numpy as np
from lib import utils, stats, checks, solve_triangular


def gauss(A, b):
    P, L, U = scipy.linalg.lu(A)
    y, _ = solve_triangular.Lsolve(L, P.T @ b)
    x, _ = solve_triangular.Usolve(U, y)
    return x


def cholesky(A, b):
    if not (checks.is_symmetrical(A) and checks.is_positive_definite(A)):
        raise ValueError("matrix not symmetrical or positive definite")
    LT = scipy.linalg.cholesky(A)
    L = LT.T
    y, _ = solve_triangular.Lsolve(L, b)
    x, _ = solve_triangular.Usolve(LT, y)
    return x


def householder(A, b):
    x = 12
    Q, R = scipy.linalg.qr(A)
    y = Q.T@b
    x, _ = solve_triangular.Usolve(R, y)
    return x


if __name__ == '__main__':
    A, b = utils.load_all()
    # checks
    assert checks.is_symmetrical(A[2]) and checks.is_positive_definite(A[2])
    assert checks.is_symmetrical(A[3]) and checks.is_positive_definite(A[3])
    # gauss
    assert ((gauss(A[0], b[0])) - np.ones_like(b[0]) < 1e-10).all()
    assert ((gauss(A[2], b[2])) - np.ones_like(b[2]) < 1e-10).all()
    assert ((gauss(A[3], b[3])) - np.ones_like(b[3]) < 1e-10).all()
    # cholesky
    assert ((cholesky(A[2], b[2])) - np.ones_like(b[2]) < 1e-10).all()
    assert ((cholesky(A[3], b[3])) - np.ones_like(b[3]) < 1e-10).all()
    # householder
    assert ((householder(A[0], b[0])) - np.ones_like(b[0]) < 1e-10).all()
    assert ((householder(A[2], b[2])) - np.ones_like(b[2]) < 1e-10).all()
    assert ((householder(A[3], b[3])) - np.ones_like(b[3]) < 1e-10).all()
