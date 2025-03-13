#!/bin/python3

import sys

sys.set_int_max_str_digits(10**9)


def euclide_gcd_rec(a, b):
    # print(a, "|", b)
    if b == 0:
        return a
    return euclide_gcd_rec(b, a % b)


def euclide_gcd_it(a, b):
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a


def euclide_extended_rec(a, b):
    if b == 0:
        return (a, 1, 0)
    d, x, y = euclide_extended_rec(b, a % b)
    return (d, y, x - a // b * y)


# def euclide_extended_it(a, b):
#     while b != 0:
#         tmp = b
#         b = a % b
#         a = tmp
#     return a


if __name__ == "__main__":
    args = sys.argv[1:]
    a = int(args[0])
    b = int(args[1])
    print(euclide_gcd_it(a, b))
    print(euclide_extended_rec(a, b))
