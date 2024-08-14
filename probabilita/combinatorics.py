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


def stirling(n, k):
    if n == k or k <= 1:
        return 1
    return stirling(n-1, k-1) + k * stirling(n-1, k)


for i in range(1, 14):
    for j in range(i, 14):
        print(stirling(j, j-i+1), end="\t")
    print()
