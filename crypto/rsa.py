#!/bin/python3

import sys
import random
import time
import os

sys.set_int_max_str_digits(10**9)

DEBUG_LEVEL = 2
if os.getenv("DBG") :
    DEBUG_LEVEL =int(os.getenv("DBG"))


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
def exp(a, b, c):
    res = a
    for i in reversed(range(b.bit_length() - 1)):
        cursor = 1 << i
        res = (res * res) % c
        if b & cursor != 0:
            res = (a * res) % c
    return res


@performance_timer(1)
def rand_ndigit_number(n):
    return random.randint(10 ** (n - 1), 10**n - 1)


@performance_timer(1)
def test_prime(n, rounds=10):
    for i in range(rounds):
        a = random.randint(1, n-1)
        x = exp(a, n - 1, n)
        if x != 1:
            return False
    return True


if __name__ == "__main__":
    print(exp(11, 2, 1000))
    for i in range(2,100):
        if test_prime(i):
            print(i) 
