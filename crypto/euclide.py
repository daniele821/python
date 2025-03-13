#!/bin/python3

import sys, time

sys.set_int_max_str_digits(10**9)


def performance_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start the timer
        result = func(*args, **kwargs)  # Call the function
        end_time = time.perf_counter()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds")
        return result  # Return the original function result

    return wrapper


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


def euclide_extended_it(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return (a, x0, y0)


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
    print(euclide_extended_it(a, b)[0])
