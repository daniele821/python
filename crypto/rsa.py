#!/bin/python3

import math
import sys
import random


def modInverse(A, M):
    if math.gcd(A, M) > 1:
        raise ValueError("numbers are not coprime!")
    for X in range(1, M):
        if ((A % M) * (X % M)) % M == 1:
            return X
    return -1


def random_coprime(n):
    m = random.randint(2, n - 1)
    while math.gcd(n, m) != 1:
        m = random.randint(2, n - 1)
        if m == 1:
            raise ValueError("ABORTING BIGGEST COPRIME")
    return m


def rsa_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random_coprime(phi)
    d = modInverse(e, phi)
    return e, n, d


def encrypt(m, e, n):
    return m**e % n


def decrypt(c, e, n):
    return c**d % n


if __name__ == "__main__":
    args = sys.argv[1:]
    p = int(args[0])
    q = int(args[1])
    text = int(args[2])
    if text >= p * q:
        raise ValueError("m too big!")
    e, n, d = rsa_key(p, q)
    print((e, n), d)
    c = encrypt(text, e, n)
    m = decrypt(c, e, n)
    print("ENCRYPT, THEN DECRYPT", text, c, m)
    m = decrypt(text, e, n)
    c = encrypt(m, e, n)
    print("ENCRYPT, THEN DECRYPT", text, m, c)
