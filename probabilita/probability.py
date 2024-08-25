from combinatorics import binomial_coefficient as bc
from fractions import Fraction


def density_binomial(n, p, k):
    if isinstance(p, str):
        p = Fraction(p)
    return bc(n, k) * (p**k) * ((1-p)**(n-k))


def density_ipergeometric(n, b, r, k):
    return Fraction(bc(b, k) * bc(r, n - k)) / Fraction(bc(r + b, n))


print(density_binomial(100, '0.85', 85).__float__())
print(density_ipergeometric(3, 4, 3, 1))
