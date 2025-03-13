#!/bin/python3

import math
import sys
import random

import euclide
import exponential


def modInverse(a, b):
    return euclide.euclide_extended_it(a, b)[1]
    


def random_coprime(n):
    m = random.randint(2, n - 1)
    while math.gcd(n, m) != 1:
        m = random.randint(2, n - 1)
        if m == 1:
            raise ValueError("ABORTING RANDOM COPRIME")
    return m


def rsa_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random_coprime(phi)
    d = modInverse(e, phi)
    return e, n, d


def encrypt(m, e, n):
    return exponential.exp(m, e, n)


def decrypt(c, e, n):
    return exponential.exp(c, d, n)


if __name__ == "__main__":
    args = sys.argv[1:]
    p = int(args[0])
    q = int(args[1])
    text = int(args[2])
    if text >= p * q:
        raise ValueError("m too big!")
    e, n, d = rsa_key(p, q)
    c = encrypt(text, e, n)
    m = decrypt(c, e, n)
    print(text)
    print(c)
    print(m)
    assert( m != text)
    m = decrypt(text, e, n)
    c = encrypt(m, e, n)
