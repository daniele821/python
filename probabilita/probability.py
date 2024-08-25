from combinatorics import binomial_coefficient as bc
from fractions import Fraction


def assert_type(variable, allowed_types):
    for types in allowed_types:
        if isinstance(variable, types):
            return
    msg = "EXPECTED TYPE = {a}, ACTUAL TYPE = {b}"
    msg = msg.format(a=allowed_types, b=str(type(variable)))
    raise TypeError(msg)


def lambda_density_binomial(n, p):
    assert_type(n, [int])
    assert_type(p, [int, str, Fraction])
    if isinstance(p, str):
        p = Fraction(p)

    def tmp(k):
        assert_type(k, [int])
        return bc(n, k) * (p**k) * ((1-p)**(n-k))
    return tmp


def lambda_density_ipergeometric(n, b, r):
    assert_type(n, [int])
    assert_type(b, [int])
    assert_type(r, [int])

    def tmp(k):
        assert_type(k, [int])
        return Fraction(bc(b, k) * bc(r, n - k)) / Fraction(bc(r + b, n))
    return tmp


def density_binomial(n, p, k):
    return lambda_density_binomial(n, p)(k)


def density_ipergeometric(n, b, r, k):
    return lambda_density_ipergeometric(n, b, r)(k)


if __name__ == "__main__":
    print(density_binomial(100, '0.85', 85).__float__())
    print(density_ipergeometric(3, 4, 3, 1))

    # bullet problem
    bullets = lambda_density_binomial(3, '0.2')
    bullsum = bullets(0) + bullets(1)
    print(bullsum, bullsum.__float__())

    # balls extraction problem
    balls = lambda_density_ipergeometric(3, 2, 8)
    basum = balls(0) + balls(1)
    print(basum, basum.__float__())
