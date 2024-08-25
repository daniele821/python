import combinatorics as cmb
from fractions import Fraction


def density_binomial(n, p, k):
    if isinstance(p, str):
        p = Fraction(p)
    return cmb.binomial_coefficient(n, k) * (p**k) * ((1-p)**(n-k))


def density_ipergeometric(n, b, r, k):
    return Fraction(cmb.binomial_coefficient(b, k) * cmb.binomial_coefficient(r, n - k)) / Fraction(cmb.binomial_coefficient(r + b, n))


print(density_binomial(100, '0.85', 85).__float__())
print(density_ipergeometric(3, 4, 3, 1))
