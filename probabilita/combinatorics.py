import sys

args = sys.argv[1:]
try:
    n = args[0]
    k = args[1]
except Exception:
    n = 10
    k = 10


def disposition(n, k):
    res = 1
    for i in range(n-k+1, n+1):
        res *= i
    return res


def factorial(n):
    return disposition(n, n-1)


def binomial_coefficient(n, k):
    return disposition(n, k) // factorial(k)


def bell(n):
    if n <= 1:
        return 1
    acc = 0
    for k in range(1, n+1):
        acc += binomial_coefficient(n-1, k-1) * bell(n - k)
    return acc


def bell2(n):
    old = [1] + [0] * (max(1, n - 1))
    new = old.copy()
    new[1] = 2
    for i in range(3, n+1):
        old[0] = new[i-2]
        for j in range(1, i):
            old[j] = new[j-1] + old[j-1]
        new = old.copy()
    if n <= 1:
        return 1
    return new[len(new) - 1]


def __print_line__(list):
    for elem in list:
        if elem == 0:
            print()
            return
        print(elem, end="\t")
    print()


def triangle_bell(size):
    old = [1] + [0] * (size)
    new = old.copy()
    new[1] = 2
    __print_line__(old)
    __print_line__(new)
    for i in range(3, size+1):
        old[0] = new[i-2]
        for j in range(1, i):
            old[j] = new[j-1] + old[j-1]
        __print_line__(old)
        new = old.copy()
    print()


def stirling(n, k):
    if n == k or k <= 1:
        return 1
    return stirling(n-1, k-1) + k * stirling(n-1, k)


def triangle_stirtling(size):
    for i in range(1, size):
        for k in range(i-1):
            print(end="\t")
        for j in range(i, size):
            print(stirling(j, i), end="\t")
        print()
    print()


def fibonacci(n):
    old = 1
    new = 1
    tmp = 69
    for i in range(n):
        tmp = new
        new = old + new
        old = tmp
    return new
