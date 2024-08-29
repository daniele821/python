# count sequences of length n, without any sequence long k of ones!
# basically the formula is:
# fibk(n) = { fibk(n-1) + ... + fibk(n-k)       if n >= k
#           { 2^n                               if 0 <= n < k


FIBONACCI3 = {}
FIBONACCI4 = {}
FIB = {}


# binary sequences where there are no sequences of 1 of len 3
def fibonacci3(n):
    if n in FIBONACCI3:
        return FIBONACCI3[n]
    tmp = None
    match n:
        case 0: tmp = 1
        case 1: tmp = 2
        case 2: tmp = 4
        case _: tmp = fibonacci3(n-1)+fibonacci3(n-2)+fibonacci3(n-3)
    FIBONACCI3[n] = tmp
    return tmp


# binary sequences where there are no sequences of 1 of len 4
def fibonacci4(n):
    if n in FIBONACCI4:
        return FIBONACCI4[n]
    tmp = None
    match n:
        case 0: tmp = 1
        case 1: tmp = 2
        case 2: tmp = 4
        case 3: tmp = 8
        case _: tmp = fibonacci4(n-1)+fibonacci4(n-2)+fibonacci4(n-3)+fibonacci4(n-4)
    FIBONACCI4[n] = tmp
    return tmp


# binary sequences where there are no sequences of 1 of len k
def fib(n, k):
    sub = "1" * k
    count = 0
    for i in range(2**n):
        if str(bin(i)).find(sub) == -1:
            # print(str(bin(i)))
            count += 1
    return count


def fib2(n, k):
    if n >= 0 and n < k:
        return 2**n
    if n >= k:
        acc = 0
        for i in range(1, k+1):
            acc += fib2(n - i, k)
        return acc


def fib3(n, k):
    if k not in FIB:
        FIB[k] = {}
    if n in FIB[k]:
        return FIB[k][n]
    if n >= 0 and n < k:
        FIB[k][n] = 2**n
        return FIB[k][n]
    if n >= k:
        acc = 0
        for i in range(1, k+1):
            acc += fib3(n - i, k)
        FIB[k][n] = acc
        return acc


for i in range(200):
    print(i, end="\t")
    print(fib3(i, 5))
