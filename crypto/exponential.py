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


def mod(num, mod):
    if mod is not None:
        return num % mod
    return num


@performance_timer
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
