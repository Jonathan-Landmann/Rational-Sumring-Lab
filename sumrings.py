"""Exact bounded experiments for N_0[q,r]; negative searches prove nothing."""
from fractions import Fraction

def rational(s: str) -> Fraction:
    return Fraction(s)

def generators(q: Fraction, r: Fraction, degree: int):
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    return sorted({q**i * r**j for i in range(degree + 1)
                   for j in range(degree + 1 - i)})

def enumerate_sumring(q: Fraction, r: Fraction, degree: int = 3,
                      coefficient_sum: int = 3, max_states: int = 200000):
    if coefficient_sum < 0 or max_states < 1:
        raise ValueError("invalid budget")
    gs = generators(q, r, degree)
    layers = [{Fraction(0)}]
    for _ in range(coefficient_sum):
        layer = {v + g for v in layers[-1] for g in gs}
        if len(layer) > max_states:
            raise RuntimeError("state limit exceeded; reduce search bounds")
        layers.append(layer)
    return set().union(*layers)

def valuation(x: Fraction, p: int) -> int:
    if p < 2 or any(p % d == 0 for d in range(2, int(p**0.5) + 1)):
        raise ValueError("p must be prime")
    if x == 0:
        raise ValueError("valuation of zero is undefined")
    def count(n):
        n = abs(n)
        c = 0
        while n % p == 0:
            n //= p
            c += 1
        return c
    return count(x.numerator) - count(x.denominator)

def prime_factors(n: int):
    n = abs(n)
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ans.append(n)
    return ans

def effective_prime_witnesses(q: Fraction, r: Fraction, exponent_bound: int = 40):
    """Find rigorous bounded witnesses; absence does not certify ineffectiveness."""
    if not (0 < q < 1 < r) or exponent_bound < 0:
        raise ValueError("requires 0 < q < 1 < r and nonnegative bound")
    primes = set(prime_factors(q.denominator) + prime_factors(r.denominator))
    found = {}
    for i in range(exponent_bound + 1):
        for j in range(exponent_bound + 1):
            x = q**i * r**j
            if x >= 1:
                continue
            for p in primes - found.keys():
                if valuation(x, p) < 0:
                    found[p] = (i, j, x)
        if len(found) == len(primes):
            break
    return found

def bounded_divisors(elements, target: Fraction):
    return sorted((d, target / d) for d in elements
                  if d != 0 and target / d in elements)

def bounded_irreducibles(elements):
    """Uncertified candidates relative only to a finite sampled set."""
    positive = sorted(x for x in elements if x > 0)
    return [x for x in positive if x != 1 and not any(
        a != 1 and x / a != 1 and x / a in elements for a in positive)]
