#!/bin/python3

import sys


def euclide_gcd(a, b):
    print(a, "|", b)
    if b == 0:
        return a
    return euclide_gcd(b, a % b)


if __name__ == "__main__":
    args = sys.argv[1:]
    a = int(args[0])
    b = int(args[1])
    print(euclide_gcd(a, b))
