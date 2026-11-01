"""Exact, independently verifiable witnesses for effective denominator primes."""
from dataclasses import dataclass
from fractions import Fraction
from effective_primes import effective_primes_exact
from sumrings import exact_rational, is_prime, positive_pair, valuation


@dataclass(frozen=True)
class EffectivePrimeCertificate:
    prime: int
    i: int
    j: int
    monomial: Fraction

    def verify(self, q: Fraction, r: Fraction) -> bool:
        """Check the defining conditions, not the decision algorithm.

        Malformed values are rejected with False. Verification uses exact
        rational arithmetic; Python floats and noninteger exponents are invalid.
        """
        try:
            q, r = positive_pair(q, r)
            monomial = exact_rational(self.monomial, "monomial")
            if not is_prime(self.prime):
                return False
            if any(isinstance(n, bool) or not isinstance(n, int) or n < 0
                   for n in (self.i, self.j)):
                return False
            return (0 < monomial < 1
                    and monomial == q**self.i * r**self.j
                    and valuation(monomial, self.prime) < 0)
        except (TypeError, ValueError):
            return False


def construct_certificate(q: Fraction, r: Fraction,
                          p: int) -> EffectivePrimeCertificate | None:
    """Return a valid certificate, or None iff p is ineffective.

    For a mixed pair x<1<y with A=v_p(x)>=0 and B=-v_p(y)>0,
    t=x**B*y**A<1. Find the least k>=1 with y*t**k<1 by doubling
    and binary search. Exponents (B*k, A*k+1) have valuation -B.
    Termination follows from t**k -> 0; this is not a polynomial-time claim.
    """
    q, r = positive_pair(q, r)
    if not is_prime(p):
        raise ValueError("p must be prime")
    if p not in effective_primes_exact(q, r):
        return None
    if q < 1 and valuation(q, p) < 0:
        return EffectivePrimeCertificate(p, 1, 0, q)
    if r < 1 and valuation(r, p) < 0:
        return EffectivePrimeCertificate(p, 0, 1, r)

    swapped = q >= 1
    x, y = (r, q) if swapped else (q, r)
    a, b = valuation(x, p), -valuation(y, p)
    t = x**b * y**a
    low, high = 0, 1
    while y * t**high >= 1:
        low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        if y * t**middle < 1:
            high = middle
        else:
            low = middle
    i, j = b * high, a * high + 1
    if swapped:
        i, j = j, i
    return EffectivePrimeCertificate(p, i, j, q**i * r**j)


def all_certificates(q: Fraction, r: Fraction) -> dict[int, EffectivePrimeCertificate]:
    q, r = positive_pair(q, r)
    return {p: construct_certificate(q, r, p)
            for p in sorted(effective_primes_exact(q, r))}
