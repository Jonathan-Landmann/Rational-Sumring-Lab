from fractions import Fraction as F
import pytest
from certificates import all_certificates, construct_certificate, EffectivePrimeCertificate
from effective_primes import effective_primes_exact


def test_named_cases():
    for q, r, expected in [
        (F(6, 35), F(19, 3), {5, 7}),
        (F(3, 10), F(7, 5), {2, 5}),
        (F(2, 5), F(2, 3), {3, 5}),
        (F(2, 3), F(3, 2), {3}),
        (F(1), F(2, 3), {3}),
        (F(1), F(1), set()),
        (F(3, 2), F(7, 5), set()),
    ]:
        for a, b in [(q, r), (r, q)]:
            certificates = all_certificates(a, b)
            assert set(certificates) == expected
            assert all(c.verify(a, b) for c in certificates.values())


def test_none_for_ineffective():
    assert construct_certificate(F(6, 35), F(19, 3), 3) is None
    assert construct_certificate(F(3, 10), F(7, 5), 3) is None
    assert construct_certificate(F(2, 3), F(3, 2), 2) is None
    assert construct_certificate(1, 2, 2) is None


@pytest.mark.parametrize('q,r,p,expected', [
    (F(2, 5), F(3, 2), 2, (1, 2, F(9, 10))),
    (F(3, 2), F(2, 5), 2, (2, 1, F(9, 10))),
    (F(99, 100), F(101, 97), 97, (5, 1, F(99, 100)**5 * F(101, 97))),
])
def test_constructive_mixed_branch(q, r, p, expected):
    c = construct_certificate(q, r, p)
    assert (c.i, c.j, c.monomial) == expected
    assert c.verify(q, r)
    assert c.monomial.denominator % p == 0


def test_tampered_certificate_rejected():
    q, r = F(6, 35), F(19, 3)
    assert EffectivePrimeCertificate(5, 1, 0, q).verify(q, r)
    assert not EffectivePrimeCertificate(5, 1, 0, F(1, 2)).verify(q, r)
    assert not EffectivePrimeCertificate(5, 0, 0, q).verify(q, r)


@pytest.mark.parametrize('p', [0, 1, 4, -5, 5.0, True, None])
def test_invalid_prime_rejected(p):
    assert not EffectivePrimeCertificate(p, 1, 0, F(1, 5)).verify(F(1, 5), 2)
    with pytest.raises(ValueError):
        construct_certificate(F(1, 5), 2, p)


@pytest.mark.parametrize('exponent', [-1, 1.0, F(1), True, None, '1'])
def test_noninteger_or_negative_exponents_rejected(exponent):
    assert not EffectivePrimeCertificate(5, exponent, 0, F(1, 5)).verify(F(1, 5), 2)
    assert not EffectivePrimeCertificate(5, 1, exponent, F(1, 5)).verify(F(1, 5), 2)


@pytest.mark.parametrize('monomial', [0, -1, 0.2, None, '1/5'])
def test_malformed_monomial_rejected(monomial):
    assert not EffectivePrimeCertificate(5, 1, 0, monomial).verify(F(1, 5), 2)


def test_verifier_rejects_invalid_base_domain():
    c = EffectivePrimeCertificate(5, 1, 0, F(1, 5))
    for q, r in [(F(1, 5), 0), (F(1, 5), -1), (0.2, 2), (True, 2), (None, 2)]:
        assert not c.verify(q, r)


def test_small_rational_grid_independent_certificate_checks():
    values = sorted({F(a, b) for a in range(1, 7) for b in range(1, 7)})
    for q in values:
        for r in values:
            certificates = all_certificates(q, r)
            assert set(certificates) == effective_primes_exact(q, r)
            for prime, c in certificates.items():
                # Direct defining-condition checks independent of verify/valuation.
                value = q**c.i * r**c.j
                assert type(c.i) is int and c.i >= 0
                assert type(c.j) is int and c.j >= 0
                assert 0 < value < 1 and value == c.monomial
                assert value.denominator % prime == 0
                assert c.verify(q, r)
