#!/bin/python3

import sys
import random
import time
import os

sys.set_int_max_str_digits(10**9)

COLOR_RED="\x1b[1;31m"
COLOR_YELLOW="\x1b[1;33m"
COLOR_NONE="\x1b[m"

DEBUG_LEVEL = 1000
if os.getenv("DBG"):
    DEBUG_LEVEL = int(os.getenv("DBG"))
LEN = 25
if os.getenv("LEN"):
    LEN = int(os.getenv("LEN"))


def performance_timer(dbgLvl=1000):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            if dbgLvl >= DEBUG_LEVEL:
                print(f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds")
            return result

        return wrapper

    return decorator


@performance_timer(0)
def exp(base, exponent, mod):
    res = base
    for i in reversed(range(exponent.bit_length() - 1)):
        cursor = 1 << i
        res = (res * res) % mod
        if exponent & cursor != 0:
            res = (base * res) % mod
    return res


@performance_timer(1)
def rand_ndigit_number(number_length_in_digits):
    return random.randint(10 ** (number_length_in_digits - 1), 10**number_length_in_digits - 1)


@performance_timer(1)
def test_prime(number, rounds=10):
    if number < 2:
        return False
    for i in range(rounds):
        a = random.randint(1, number - 1)
        x = exp(a, number - 1, number)
        if x != 1:
            return False
    return True


@performance_timer(2)
def rand_prime_number(number_length_in_digits):
    while True:
        number = rand_ndigit_number(number_length_in_digits)
        if test_prime(number):
            return number


@performance_timer(1)
def euclide_gcd_it(a, b):
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a


@performance_timer(1)
def euclide_extended_it(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return (a, x0, y0)


@performance_timer(2)
def rand_public_key(phi):
    while True:
        e = random.randint(2, phi)
        if euclide_gcd_it(phi, e) == 1:
            return e


@performance_timer(2)
def private_key(e, phi):
    return (euclide_extended_it(e, phi)[1] + phi) % phi


if __name__ == "__main__":
    p = rand_prime_number(LEN)
    print(f"p: {p}")
    q = rand_prime_number(LEN)
    print(f"q: {q}")
    n = p * q
    print(f"n: {n}")
    phi = (p - 1) * (q - 1)
    print(f"φ: {phi}")
    e = rand_public_key(phi)
    print(f"e: {e}")
    d = private_key(e, phi)
    print(f"d: {d}")

    print("\nENCRYPTION:")
    m = rand_ndigit_number(LEN // 2)
    print(f"m: {COLOR_RED}{m}{COLOR_NONE}")
    c = exp(m, e, n)
    print(f"c: {c}")
    m = exp(c, d, n)
    print(f"m: {COLOR_RED}{m}{COLOR_NONE}")

    print("\nDECRYPTION:")
    print(f"m: {COLOR_YELLOW}{m}{COLOR_NONE}")
    c = exp(m, d, n)
    print(f"c: {c}")
    m = exp(c, e, n)
    print(f"m: {COLOR_YELLOW}{m}{COLOR_NONE}")

