#!/bin/python3

import numpy as np


def info(A):
    size = A.size
    non_zeros = np.count_nonzero(A)
    zeros = size - non_zeros
    density = zeros / size
    print("matrix shape: {}".format(A.shape))
    print("matrix zeros: {}/{} -> {}".format(zeros, size, density))


if __name__ == "__main__":
    size = 5000
    A = np.random.rand(size, size)
    info(A)
    print('methods were successfully tested!')
