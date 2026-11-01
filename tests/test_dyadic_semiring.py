from fractions import Fraction as F
import pytest

from dyadic_semiring import (
    Q, R, CONDUCTOR, PolynomialCertificate, binary_prefix,
    conductor_certificate, is_localized, parity, tau,
)


def test_domain_and_parity():
    for value in [0, -1, F(-7, 135), F(11, 625), F(1, 15**20)]:
        assert is_localized(value)
        assert parity(value) in (0, 1)
        assert is_localized(tau(value))
    for value in [F(1, 2), F(1, 7), 0.2, True, '1/5']:
        assert not is_localized(value)
        with pytest.raises((TypeError, ValueError)):
            tau(value)


def test_binary_prefix_reconstruction_including_negative_inputs():
    for value in [F(-17, 75), F(0), F(27, 25), F(5, 3), F(3**9, 5**7)]:
        for length in range(13):
            digits, residual = binary_prefix(value, length)
            assert set(digits) <= {0, 1}
            assert value == sum((digit * Q**i for i, digit in enumerate(digits)), F(0)) + Q**length * residual


@pytest.mark.parametrize('length', [-1, 1.0, True])
def test_invalid_prefix_length(length):
    with pytest.raises(ValueError):
        binary_prefix(F(5, 3), length)


def test_conductor_certificate_grid_independent_evaluation():
    # Direct polynomial evaluation checks witnesses, not the generating algorithm.
    for a in range(5):
        for b in range(5):
            denominator = 3**a * 5**b
            first = (5 * denominator + 2) // 3
            for numerator in range(first, first + 17):
                value = F(numerator, denominator)
                certificate = conductor_certificate(value)
                evaluated = sum((c * F(2, 5)**i * F(2, 3)**j
                                 for c, i, j in certificate.terms), F(0))
                assert evaluated == value
                assert certificate.verify(value)


def test_high_denominator_and_boundary_certificates():
    for value in [CONDUCTOR, CONDUCTOR + F(1, 15**30), F(20, 3),
                  F(20, 3) + F(1, 3**40 * 5**35), F(10**30 + 1, 3**12 * 5**8)]:
        assert conductor_certificate(value).verify(value)
    assert conductor_certificate(CONDUCTOR).terms == ((1, 0, 0), (1, 0, 1))
    with pytest.raises(ValueError):
        conductor_certificate(CONDUCTOR - F(1, 15))
    with pytest.raises(ValueError):
        conductor_certificate(F(17, 7))


@pytest.mark.parametrize('terms', [
    ((-1, 0, 0),), ((1, -1, 0),), ((True, 0, 0),), ((1, 0.0, 0),),
    ((1, 0),), None, [(1, 0, 0)],
])
def test_malformed_polynomial_certificates_rejected(terms):
    assert not PolynomialCertificate(terms).verify(1)


def test_tampered_polynomial_and_inexact_target_rejected():
    certificate = conductor_certificate(F(7, 3))
    assert not certificate.verify(F(7, 3) + 1)
    assert not certificate.verify(float(F(7, 3)))


def test_sharp_boundary_obstructions():
    # tau preserves S; a negative residual is a rigorous finite nonmembership obstruction.
    for n in range(1, 18):
        value = CONDUCTOR - 2 * Q**n
        digits, residual = binary_prefix(value, n)
        assert 0 < value < CONDUCTOR
        assert digits == (1,) * n
        assert residual == F(-1, 3)
    assert tau(F(27, 25)) == F(1, 5)
    assert tau(tau(F(27, 25))) == -2


def test_prefix_congruence_exact_finite_cases():
    # Congruence modulo 2**length fixes that many digits; q has valuation one.
    for length in range(1, 13):
        for value in [F(5, 3), F(19, 15), F(83, 75), F(27, 25)]:
            perturbation = F(2**length, 3**4 * 5**3)
            digits, residual = binary_prefix(value, length)
            other_digits, other_residual = binary_prefix(value + perturbation, length)
            assert other_digits == digits
            assert other_residual - residual == perturbation / Q**length


def test_rewrite_and_atom_family_finite_hypotheses():
    assert R == Q + Q * R
    for n in range(16):
        value = 1 + Q**n * R
        certificate = PolynomialCertificate(((1, 0, 0), (1, n, 1)))
        assert certificate.verify(value)
        # The paper proves the infinite atom family. These check its finite identities.
        assert value.denominator % 3 == 0
        assert value.denominator % 9 != 0
        digits, residual = binary_prefix(value, n + 1)
        assert digits == (1,) + (0,) * n
        assert residual == CONDUCTOR
        assert tau(residual) == residual


def test_double_summand_digit_identity():
    # A coefficient >=2 forces a residual >5/3, the paper's atom obstruction.
    for n in range(12):
        for remainder in [F(0), Q, R, 1 + Q**3 * R, Q**2 + R**3]:
            digits, residual = binary_prefix(remainder, n)
            other_digits, other_residual = binary_prefix(2 * Q**n + remainder, n)
            assert other_digits == digits
            assert other_residual == 2 + residual
            assert other_residual > CONDUCTOR


def test_membership_named_cases_and_rejection_evidence():
    from dyadic_semiring import decide_membership
    for value in [F(0), F(1), Q, R, CONDUCTOR, F(3), F(729, 625), F(49, 27)]:
        result = decide_membership(value)
        assert result.is_member and result.certificate.verify(value)
        assert result.verify(value)
    result = decide_membership(F(27, 25))
    assert not result.is_member and result.reason == 'negative_iterate'
    assert result.trajectory == (F(27, 25), F(1, 5), F(-2))
    assert result.verify(F(27, 25))
    for value in [F(-1), F(1, 2), F(1, 7), F(3125, 2187)]:
        result = decide_membership(value)
        assert not result.is_member and result.verify(value)
    for n in range(1, 18):
        value = CONDUCTOR - 2 * Q**n
        result = decide_membership(value)
        assert not result.is_member and result.verify(value)


def test_membership_accepts_independent_polynomial_sum_grid():
    from itertools import combinations_with_replacement
    from dyadic_semiring import decide_membership
    # Construct values directly from nonnegative polynomials, not the decision code.
    monomials = [F(2, 5)**i * F(2, 3)**j for i in range(4) for j in range(4 - i)]
    values = {sum(terms, F(0)) for size in range(4)
              for terms in combinations_with_replacement(monomials, size)}
    for value in values:
        result = decide_membership(value)
        assert result.is_member
        assert result.certificate.verify(value)


def test_membership_grid_evidence_checked_separately():
    from dyadic_semiring import decide_membership
    counts = {True: 0, False: 0}
    for a in range(3):
        for b in range(3):
            denominator = 3**a * 5**b
            for numerator in range(-2, 2 * denominator + 1):
                value = F(numerator, denominator)
                result = decide_membership(value)
                assert result.verify(value)
                if result.is_member:
                    # Independent exact evaluation of its polynomial witness.
                    actual = sum((c * F(2, 5)**i * F(2, 3)**j
                                  for c, i, j in result.certificate.terms), F(0))
                    assert actual == value
                else:
                    # A finite negative tau iterate is independently sound by closure.
                    # Cycle cases, if any, additionally require the paper's normal-form theorem.
                    assert result.reason in {'negative_iterate', 'cycle'}
                counts[result.is_member] += 1
    assert counts[True] > 0 and counts[False] > 0


def test_tampered_membership_evidence_rejected():
    from dataclasses import replace
    from dyadic_semiring import MembershipResult, decide_membership
    valid = decide_membership(F(27, 25))
    assert not replace(valid, trajectory=(F(27, 25), F(-2))).verify(F(27, 25))
    assert not replace(valid, trajectory=(F(27, 25),)).verify(F(27, 25))
    assert not replace(valid, reason='outside_localization').verify(F(27, 25))
    assert not replace(valid, is_member=True).verify(F(27, 25))
    assert not MembershipResult(False, 'cycle', None, (CONDUCTOR, CONDUCTOR)).verify(CONDUCTOR)
    assert not MembershipResult(False, 'cycle', None, (F(0), F(0))).verify(0)
    assert not MembershipResult(False, 'cycle', None, (F(1), F(1))).verify(1)
    assert not MembershipResult(False, 'cycle', None, (F(1, 2), F(1, 2))).verify(F(1, 2))
    with pytest.raises(TypeError):
        decide_membership(0.2)
