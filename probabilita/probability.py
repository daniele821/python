import combinatorics as cmb


def lambda_density_binomial(n, p):
    return lambda k: cmb.binomial_coefficient(n, k) * (p**k) * ((1-p)**(n-k))


def density_binomial(n, p, k):
    return lambda_density_binomial(n, p)(k)


print(density_binomial(100, 0.85, 85))
