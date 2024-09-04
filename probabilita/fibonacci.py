# THE FOLLOWING FORMULAS ARE A PERSONAL BREAK THROUGH!
# they are not mathematically proven to be correct, but they likely are!

# FORMULA:
# count sequences of length n, without any sequence long k of ones!
# basically the formula is:
# fibk(n) = { fibk(n-1) + ... + fibk(n-k)       if n >= k
#           { 2^n                               if 0 <= n < k

import sys
from fractions import Fraction

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
def fib1(n, k):
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


def fib(n, k):
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
            acc += fib(n - i, k)
        FIB[k][n] = acc
        return acc


# solves the following problem:
#  what is the probabilty of getting a sequence of 'seq_len' successes
#  for the 1st time after 'throws' amount of throws
# EXAMPLE:
#  - throws = 10
#  - seq_len = 4
#    what is the probability of the following: _ _ _ _ _ N S S S S
#    where:
#    - S means a success
#    - N means an insuccess
#    - _ means either N or S
# to calculate that, we use the formula for the uniforme probability:
#   | # successful results | / | # all the possible results |
# to calculate all possible results, it's the sequences of 2, 'throws' long:
#   2^'throws'
# to calculate the successfull results, we have:
#   - a single final sequence of 'throws' S
#   - the value before MUST be N
#   - all the possible combination of lenght 'throws' - 'seq_len' - 1
#     which have no sequence of 1 longer or equal to 'seq_len'.
#     That can be calculate using fibk(n) defined before!

def prob(throws, seq_len):
    if throws < seq_len:
        return 0
    all_results = 2**throws
    pos_results = 1
    if throws > seq_len:
        pos_results = fib(throws - seq_len - 1, seq_len)
    return Fraction("{}/{}".format(pos_results, all_results))


# formula: E[X] = 2^k - 2
# - X is the aleatory variable which represents the quantity of coin throws
#   needed to get the first sequence of lenght k of consecutive 1
# - E[X] is the expected value of the X aleatory variable
# the following code makes a calculation based "proof" of the formula:
if __name__ == "__main__":
    K = 10
    sys.set_int_max_str_digits(1_000_000)
    sum = 0
    for i in range(100000):
        density = prob(i, K)
        sum += density * i
        print(sum.__float__(), i)
