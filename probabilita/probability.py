from combinatorics import binomial_coefficient as bc
from fractions import Fraction


def assert_type(variable, allowed_types):
    for types in allowed_types:
        if isinstance(variable, types):
            return
    msg = "EXPECTED TYPES = {a}, ACTUAL TYPE = {b}"
    msg = msg.format(a=allowed_types, b=str(type(variable)))
    raise TypeError(msg)


def lambda_density_binomial(n, p):
    assert_type(n, [int])
    assert_type(p, [int, str, Fraction])
    if isinstance(p, str):
        p = Fraction(p)

    def tmp(k):
        assert_type(k, [int])
        if k < 0:
            return 0
        return Fraction(bc(n, k) * (p**k) * ((1-p)**(n-k)))
    return tmp


def lambda_density_ipergeometric(n, b, r):
    assert_type(n, [int])
    assert_type(b, [int])
    assert_type(r, [int])

    def tmp(k):
        assert_type(k, [int])
        minval = max(0, n - r)
        maxval = min(n, b)
        if minval > maxval or k < minval or k > maxval:
            return 0
        return Fraction(bc(b, k) * bc(r, n - k)) / Fraction(bc(r + b, n))
    return tmp


def lambda_density_geometric_modified(p):
    assert_type(p, [int, str, Fraction])
    if isinstance(p, str):
        p = Fraction(p)

    def tmp(k):
        assert_type(k, [int])
        if k < 1:
            return 0
        return Fraction((1-p)**(k-1) * p)
    return tmp


def lambda_density_geometric(p):
    assert_type(p, [int, str, Fraction])
    if isinstance(p, str):
        p = Fraction(p)

    def tmp(k):
        assert_type(k, [int])
        if k < 0:
            return 0
        return Fraction((1-p)**(k) * p)
    return tmp


def density_binomial(n, p, k):
    return lambda_density_binomial(n, p)(k)


def density_ipergeometric(n, b, r, k):
    return lambda_density_ipergeometric(n, b, r)(k)


def density_geometric_modified(p, k):
    return lambda_density_geometric_modified(p)(k)


def density_geometric(p, k):
    return lambda_density_geometric(p)(k)


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

    gemod = lambda_density_geometric_modified("0.6")
    for i in range(4):
        print(gemod(i))
