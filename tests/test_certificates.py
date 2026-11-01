from fractions import Fraction as F
from certificates import all_certificates, construct_certificate, EffectivePrimeCertificate
from effective_primes import effective_primes_exact

def test_named_cases():
    for q, r, expected in [
        (F(6,35), F(19,3), {5,7}),
        (F(3,10), F(7,5), {2,5}),
        (F(2,5), F(2,3), {3,5}),
        (F(2,3), F(3,2), {3}),
    ]:
        certificates = all_certificates(q, r)
        assert set(certificates) == expected
        assert all(c.verify(q, r) for c in certificates.values())

def test_none_for_ineffective():
    assert construct_certificate(F(6,35), F(19,3), 3) is None
    assert construct_certificate(F(3,10), F(7,5), 3) is None

def test_tampered_certificate_rejected():
    c = EffectivePrimeCertificate(5, 1, 0, F(6,35))
    assert c.verify(F(6,35), F(19,3))
    assert not EffectivePrimeCertificate(5, 1, 0, F(1,2)).verify(F(6,35), F(19,3))

def test_small_rational_grid():
    for a in range(1,5):
        for b in range(a+1,7):
            for c in range(2,7):
                for d in range(1,c):
                    q,r=F(a,b),F(c,d)
                    certificates=all_certificates(q,r)
                    assert set(certificates)==effective_primes_exact(q,r)
                    assert all(z.verify(q,r) for z in certificates.values())
