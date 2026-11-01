"""Exact effective denominator primes for any positive rational pair.

For x < 1 < y, put A=v_p(x), C=v_p(y). Then p is effective iff
A<0 or (A>=0, C<0, x**(-C)*y**A<1). The other regimes are elementary.
See PROOF.md and the paper for scope, proof, and lack of a novelty claim.
"""
from fractions import Fraction
from sumrings import positive_pair, valuation, prime_factors


def effective_primes_exact(q: Fraction, r: Fraction) -> set[int]:
    q, r = positive_pair(q, r)
    if q >= 1 and r >= 1:
        return set()
    primes = set(prime_factors(q.denominator) + prime_factors(r.denominator))
    if q <= 1 and r <= 1:
        return primes
    x, y = (q, r) if q < 1 else (r, q)
    effective = set()
    for p in primes:
        a, c = valuation(x, p), valuation(y, p)
        if a < 0 or (a >= 0 and c < 0 and x**(-c) * y**a < 1):
            effective.add(p)
    return effective
