"""Exact characterization of effective denominator primes.

For 0<q<1<r and prime p, put A=v_p(q), C=v_p(r).
Then p is effective iff A<0 or (A>=0, C<0, q**(-C)*r**A<1).
No floating point and no exponent cutoff.
"""
from fractions import Fraction
from sumrings import valuation, prime_factors

def effective_primes_exact(q: Fraction, r: Fraction):
    if not (0 < q < 1 < r):
        raise ValueError("require 0 < q < 1 < r")
    primes = set()
    for n in (q.numerator, q.denominator, r.numerator, r.denominator):
        primes.update(prime_factors(n))
    effective = set()
    for p in primes:
        a, c = valuation(q, p), valuation(r, p)
        if a < 0 or (a >= 0 and c < 0 and q**(-c) * r**a < 1):
            effective.add(p)
    return effective
