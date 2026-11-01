"""Finite exact checks accompanying the paper's proof; not an atomicity solver.

Run from any working directory with Python 3.10+. No third-party dependencies.
The general conductor, atom restrictions, and non-atomicity conclusions require
and are established by the written proofs, not by these finite computations.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dyadic_semiring import (
    Q, R, CONDUCTOR, PolynomialCertificate, binary_prefix,
    conductor_certificate, decide_membership, tau,
)


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def conductor_checks():
    count = 0
    for a in range(5):
        for b in range(5):
            denominator = 3**a * 5**b
            first = (5 * denominator + 2) // 3
            for numerator in range(first, first + 17):
                value = F(numerator, denominator)
                certificate = conductor_certificate(value)
                # Direct independent evaluation, without calling certificate.verify.
                actual = sum((c * F(2, 5)**i * F(2, 3)**j
                              for c, i, j in certificate.terms), F(0))
                require(actual == value, "conductor certificate evaluates exactly")
                require(all(type(n) is int and n >= 0 for term in certificate.terms for n in term),
                        "all certificate data are nonnegative integers")
                count += 1
    for value in [CONDUCTOR + F(1, 15**30), F(20, 3) + F(1, 3**40 * 5**35)]:
        require(conductor_certificate(value).verify(value), "high-denominator certificate")
    require(count == 425, "reproducible conductor grid size")
    return count


def digit_and_boundary_checks():
    require(R == Q + Q * R, "r = q + qr")
    require(tau(CONDUCTOR) == CONDUCTOR, "5/3 is a digit-map fixed point")
    for n in range(1, 18):
        digits, residual = binary_prefix(CONDUCTOR - 2 * Q**n, n)
        require(digits == (1,) * n and residual == F(-1, 3),
                "sharp-boundary nonmembership obstruction")
    require(tau(F(27, 25)) == F(1, 5), "first obstruction digit for 27/25")
    require(tau(tau(F(27, 25))) == -2, "negative residual for 27/25")
    count = 0
    for n in range(12):
        for remainder in [F(0), Q, R, 1 + Q**3 * R, Q**2 + R**3]:
            digits, residual = binary_prefix(remainder, n)
            other_digits, other_residual = binary_prefix(2 * Q**n + remainder, n)
            require(digits == other_digits and other_residual == residual + 2,
                    "double-summand digit identity")
            require(other_residual > CONDUCTOR, "atom-obstruction residual exceeds conductor")
            count += 1
    return count


def atom_family_checks():
    # These prove finite identities only; atomhood follows from the paper's argument.
    for n in range(16):
        value = 1 + Q**n * R
        require(PolynomialCertificate(((1, 0, 0), (1, n, 1))).verify(value),
                "displayed atom-family membership identity")
        digits, residual = binary_prefix(value, n + 1)
        require(digits == (1,) + (0,) * n and residual == CONDUCTOR,
                "displayed atom-family prefix reaches the fixed point")
        require(value.denominator % 3 == 0 and value.denominator % 9 != 0,
                "displayed atom-family reduced denominator has one factor of three")
    return 16


def high_r_degree_checks():
    count = 0
    for i in range(6):
        for j in range(2, 7):
            # r**j = q**j*(1+r)**j. Split two copies of q**(i+j)*r
            # using r=q+qr; this isolates 2*q**(i+j+1) with nonnegative remainder.
            terms = [(comb(j, k) - (2 if k == 1 else 0), i + j, k)
                     for k in range(j + 1)]
            terms.append((2, i + j + 1, 1))
            remainder = PolynomialCertificate(tuple(terms))
            require(remainder.verify(Q**i * R**j - 2 * Q**(i + j + 1)),
                    "high-r-degree monomial has an explicit double-q summand")
            count += 1
    return count


def weight_candidate_checks():
    candidates = [(b, F(3)**(b + 1) / F(5)**b) for b in range(13)
                  if 1 < F(3)**(b + 1) / F(5)**b <= CONDUCTOR]
    require(candidates == [(2, F(27, 25))], "finite weight-one candidate check")
    require(CONDUCTOR == F(5, 3), "technical denominator-three candidate")
    # The proof rules out every larger b by monotonicity, not by this finite bound.


def membership_checks():
    monomials = [F(2, 5)**i * F(2, 3)**j for i in range(4) for j in range(4 - i)]
    values = {sum(terms, F(0)) for size in range(4)
              for terms in combinations_with_replacement(monomials, size)}
    for value in values:
        result = decide_membership(value)
        require(result.is_member and result.certificate.verify(value),
                "independently constructed polynomial is accepted with a witness")
    require(len(values) == 233, "reproducible independent polynomial grid size")
    counts = {True: 0, False: 0}
    for a in range(3):
        for b in range(3):
            denominator = 3**a * 5**b
            for numerator in range(-2, 2 * denominator + 1):
                value = F(numerator, denominator)
                result = decide_membership(value)
                require(result.verify(value), "membership evidence verifies independently")
                counts[result.is_member] += 1
    require(counts == {True: 512, False: 321}, "reproducible membership grid counts")
    return len(values), counts


def main():
    conductor_count = conductor_checks()
    digit_count = digit_and_boundary_checks()
    family_count = atom_family_checks()
    high_r_count = high_r_degree_checks()
    weight_candidate_checks()
    polynomial_count, membership_counts = membership_checks()
    print(f"PASS: {conductor_count} conductor certificates and two high-denominator examples.")
    print("PASS: 17 sharp-boundary obstructions and exact nonmembership of 27/25.")
    print(f"PASS: {digit_count} double-summand digit identities.")
    print(f"PASS: {high_r_count} explicit high-r-degree nonnegative remainder certificates.")
    print(f"PASS: {family_count} finite atom-family identities and the weight-one candidate check.")
    print(f"PASS: {polynomial_count} independently constructed polynomial members.")
    print(f"PASS: {sum(membership_counts.values())} membership decisions with checked evidence "
          f"({membership_counts[True]} positive, {membership_counts[False]} negative).")
    print("These finite checks support the written proofs. They do not independently")
    print("establish the general non-atomicity theorem or resolve IDF.")


if __name__ == '__main__':
    main()
