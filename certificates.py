"""Exact, independently verifiable certificates for effective denominator primes."""
from dataclasses import dataclass
from fractions import Fraction
from effective_primes import effective_primes_exact
from sumrings import valuation

@dataclass(frozen=True)
class EffectivePrimeCertificate:
    prime: int
    i: int
    j: int
    monomial: Fraction

    def verify(self, q: Fraction, r: Fraction) -> bool:
        return (self.i >= 0 and self.j >= 0
                and self.monomial == q ** self.i * r ** self.j
                and self.monomial < 1
                and valuation(self.monomial, self.prime) < 0)

def construct_certificate(q: Fraction, r: Fraction, p: int) -> EffectivePrimeCertificate | None:
    """Guaranteed to terminate for effective p; exact rational comparisons only."""
    if p not in effective_primes_exact(q, r):
        return None
    a = valuation(q, p)
    if a < 0:
        cert = EffectivePrimeCertificate(p, 1, 0, q)
        assert cert.verify(q, r)
        return cert
    b = -valuation(r, p)
    assert b > 0
    i = 1
    while True:
        j = (a * i) // b + 1
        x = q ** i * r ** j
        if x < 1:
            cert = EffectivePrimeCertificate(p, i, j, x)
            assert cert.verify(q, r)
            return cert
        i += 1

def all_certificates(q: Fraction, r: Fraction):
    return {p: construct_certificate(q, r, p)
            for p in sorted(effective_primes_exact(q, r))}
