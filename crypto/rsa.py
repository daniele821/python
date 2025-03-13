#!/bin/python3

import sys
import random
import time
import os

sys.set_int_max_str_digits(10**9)

COLOR_RED = "\x1b[1;31m"
COLOR_BLUE = "\x1b[1;34m"
COLOR_GREEN = "\x1b[1;32m"
COLOR_NONE = "\x1b[m"

DEBUG_LEVEL = 1000
if os.getenv("DBG"):
    DEBUG_LEVEL = int(os.getenv("DBG"))
LEN = 25
if os.getenv("LEN"):
    LEN = int(os.getenv("LEN"))
BASE = 10
if os.getenv("BASE"):
    BASE = int(os.getenv("BASE"))


def to_base(n):
    if BASE > 36:
        raise ValueError("base too big!")
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digit = n % BASE
        if digit >= 10:
            digit = digit + ord("a") - 10
        else:
            digit += ord('0')
        digits.append(str(chr(digit)))
        n //= BASE
    return "".join(digits[::-1])


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
    return random.randint(BASE ** (number_length_in_digits - 1), BASE**number_length_in_digits - 1)


@performance_timer(1)
def test_prime(number, rounds=3):
    if number < 2:
        return False
    for i in range(rounds):
        a = random.randint(1, number - 1)
        x = exp(a, number - 1, number)
        if x != 1:
            return False
    return True


@performance_timer(1)
def test_prime_faster(n, k=3):
    """Probabilistic primality test using Miller-Rabin."""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, min(n - 2, 1 << 30))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


@performance_timer(2)
def rand_prime_number(number_length_in_digits):
    while True:
        number = rand_ndigit_number(number_length_in_digits)
        if number % 2 == 0:
            number += 1
        if test_prime_faster(number):
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
    print(f"p: {to_base(p)}")
    q = rand_prime_number(LEN)
    print(f"q: {to_base(q)}")
    n = p * q
    print(f"n: {to_base(n)}")
    phi = (p - 1) * (q - 1)
    print(f"φ: {to_base(phi)}")
    e = rand_public_key(phi)
    print(f"e: {to_base(e)}")
    d = private_key(e, phi)
    print(f"d: {to_base(d)}")

    print("\nENCRYPTION:")
    m = rand_ndigit_number(LEN // 2)
    print(f"m: {COLOR_RED}{to_base(m)}{COLOR_NONE}")
    c = exp(m, e, n)
    print(f"c: {COLOR_BLUE}{to_base(c)}{COLOR_NONE}")
    m = exp(c, d, n)
    print(f"m: {COLOR_RED}{to_base(m)}{COLOR_NONE}")

    print("\nDECRYPTION:")
    print(f"m: {COLOR_RED}{to_base(m)}{COLOR_NONE}")
    c = exp(m, d, n)
    print(f"c: {COLOR_GREEN}{to_base(c)}{COLOR_NONE}")
    m = exp(c, e, n)
    print(f"m: {COLOR_RED}{to_base(m)}{COLOR_NONE}")
