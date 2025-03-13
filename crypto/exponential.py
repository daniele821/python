#!/bin/python3

import sys

# a^b mod c


def mod(num, mod):
    if mod is not None:
        return num % mod
    return num


def exp(a, b, c):
    res = a
    for i in reversed(range(b.bit_length() - 1)):
        cursor = 1 << i
        res = mod(res * res, c)
        if b & cursor != 0:
            res = mod(a * res, c)
    return res


if __name__ == "__main__":
    args = sys.argv[1:]
    a = int(args[0])
    b = int(args[1])
    c = None
    if len(args) > 2:
        c = int(args[2])
    print(exp(a, b, c))
    # print(mod(a**b, c))
