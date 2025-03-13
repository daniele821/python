#!/bin/python3

import sys
import random
import time
import os

sys.set_int_max_str_digits(10**9)

DEBUG_LEVEL = 2
if os.getenv("DBG"):
    DEBUG_LEVEL = int(os.getenv("DBG"))


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
def test_prime(number, rounds=3):
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


if __name__ == "__main__":
    p = rand_prime_number(50)
    print(f'p: {p}')
    q = rand_prime_number(50)
    print(f'q: {q}')
    n = p * q
    phi = (p-1) * (q-1)
