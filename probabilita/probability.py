from combinatorics import binomial_coefficient as bc
from fractions import Fraction


def lambda_density_binomial(n, p):
    if isinstance(p, str):
        p = Fraction(p)
    return lambda k: bc(n, k) * (p**k) * ((1-p)**(n-k))


def lambda_density_ipergeometric(n, b, r):
    return lambda k: Fraction(bc(b, k) * bc(r, n - k)) / Fraction(bc(r + b, n))


def density_binomial(n, p, k):
    return lambda_density_binomial(n, p)(k)


def density_ipergeometric(n, b, r, k):
    return lambda_density_ipergeometric(n, b, r)(k)


print(density_binomial(100, '0.85', 85).__float__())
print(density_ipergeometric(3, 4, 3, 1))

# bullet problem
bullets = lambda_density_binomial(3, '0.2')
bullsum = bullets(0) + bullets(1)
print(bullsum, bullsum.__float__())
