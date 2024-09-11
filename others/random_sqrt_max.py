#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt

N = 50


def plot_rand(rand_arr):
    subgrp = [0] * N
    for elem in rand_arr:
        elem = elem * N
        subgrp[int(elem)] += 1
    plt.bar(np.arange(N), subgrp)
    plt.pause(1)
    plt.clf()


X = np.random.rand(100_000)
Y = np.random.rand(100_000)
plot_rand(np.maximum(X, Y))
plot_rand(np.sqrt(X))
