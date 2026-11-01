"""Exact certificates for S = N_0[2/5, 2/3].

The paper proves the digit reduction, sharp conductor 5/3, and terminating
membership procedure. Positive answers carry finite polynomial witnesses;
negative answers carry an exact rejection trace. This is not an atom or IDF
solver, and no polynomial-time or bounded-resource claim is made.
"""
from dataclasses import dataclass
from fractions import Fraction

from sumrings import exact_rational, nonnegative_integer

Q = Fraction(2, 5)
R = Fraction(2, 3)
CONDUCTOR = Fraction(5, 3)
COARSE_CONDUCTOR = Fraction(20, 3)


def is_localized(value) -> bool:
    """Whether value is an exact element of Z[1/15] (signed values allowed)."""
    try:
        value = exact_rational(value)
    except TypeError:
        return False
    denominator = value.denominator
    for prime in (3, 5):
        while denominator % prime == 0:
            denominator //= prime
    return denominator == 1


def localized(value) -> Fraction:
    value = exact_rational(value)
    if not is_localized(value):
        raise ValueError("value must lie in Z[1/15]")
    return value


def parity(value) -> int:
    """The residue in {0,1}; every allowed denominator is odd."""
    return localized(value).numerator % 2


def tau(value) -> Fraction:
    """Return (value - parity(value))/(2/5), exactly in Z[1/15]."""
    value = localized(value)
    return (value - value.numerator % 2) / Q


def binary_prefix(value, length: int) -> tuple[tuple[int, ...], Fraction]:
    """Return the first length digits and the residual tau**length(value).

    This is a rational identity, not a membership conclusion. In particular,
    digits can also be computed for negative elements outside the semiring.
    """
    value = localized(value)
    nonnegative_integer(length, "length")
    digits = []
    for _ in range(length):
        digit = value.numerator % 2
        digits.append(digit)
        value = (value - digit) / Q
    return tuple(digits), value


@dataclass(frozen=True)
class PolynomialCertificate:
    """Terms (nonnegative coefficient, q exponent, r exponent)."""
    terms: tuple[tuple[int, int, int], ...]

    def verify(self, target) -> bool:
        """Independently evaluate a finite nonnegative polynomial at (2/5,2/3)."""
        try:
            target = exact_rational(target, "target")
            if not isinstance(self.terms, tuple):
                return False
            value = Fraction(0)
            for term in self.terms:
                if not isinstance(term, tuple) or len(term) != 3:
                    return False
                if any(isinstance(n, bool) or not isinstance(n, int) or n < 0
                       for n in term):
                    return False
                coefficient, i, j = term
                value += coefficient * Q**i * R**j
            return value == target
        except (TypeError, ValueError):
            return False


def _prepend_digits(digits, certificate: PolynomialCertificate) -> PolynomialCertificate:
    shift = len(digits)
    terms = [(digit, i, 0) for i, digit in enumerate(digits) if digit]
    terms += [(coefficient, i + shift, j) for coefficient, i, j in certificate.terms]
    return PolynomialCertificate(tuple(terms))


def _denominator_exponents(value: Fraction) -> tuple[int, int]:
    denominator = value.denominator
    exponents = []
    for prime in (3, 5):
        exponent = 0
        while denominator % prime == 0:
            denominator //= prime
            exponent += 1
        exponents.append(exponent)
    if denominator != 1:
        raise ValueError("value must lie in Z[1/15]")
    return tuple(exponents)


def _residue_digits(value: Fraction, prime: int, degree: int):
    """Represent a residue mod Z with digits 0..prime-1 in powers of 2/prime."""
    base = Fraction(2, prime)
    digits = []
    representative = Fraction(0)
    for power in range(degree, 0, -1):
        scaled = value * prime**power
        if scaled.denominator != 1:
            raise ArithmeticError("residue reduction lost its denominator invariant")
        digit = scaled.numerator * pow(pow(2, power, prime), -1, prime) % prime
        if digit:
            digits.append((digit, power))
            contribution = digit * base**power
            representative += contribution
            value -= contribution
    if value.denominator != 1:
        raise ArithmeticError("residue reduction did not finish at an integer")
    return digits, representative


def _coarse_certificate(value: Fraction) -> PolynomialCertificate:
    """CRT plus finite base-2/5 and base-2/3 residue expansions."""
    if value < COARSE_CONDUCTOR:
        raise ValueError("coarse construction requires value >= 20/3")
    a, b = _denominator_exponents(value)
    three, five = 3**a, 5**b
    numerator = value.numerator
    alpha = numerator * pow(three, -1, five) % five if b else 0
    # alpha/5**b + beta/3**a agrees with value modulo Z.
    beta = ((numerator - alpha * three) // five) % three if a else 0
    q_digits, q_residue = _residue_digits(Fraction(alpha, five), 5, b)
    r_digits, r_residue = _residue_digits(Fraction(beta, three), 3, a)
    integer_part = value - q_residue - r_residue
    if integer_part.denominator != 1 or integer_part < 0:
        raise ArithmeticError("the nonnegative CRT remainder invariant failed")
    terms = [(digit, power, 0) for digit, power in q_digits]
    terms += [(digit, 0, power) for digit, power in r_digits]
    if integer_part:
        terms.append((integer_part.numerator, 0, 0))
    return PolynomialCertificate(tuple(sorted(terms, key=lambda term: (term[1], term[2]))))


def conductor_certificate(value) -> PolynomialCertificate:
    """Construct a membership certificate for every localized value >= 5/3.

    Digit reduction reaches 20/3 because tau(x)-5/3 >= (5/2)(x-5/3)
    for x>5/3. Reverse the finite digit prefix after the coarse CRT construction.
    The exact boundary 5/3 has the certificate 1+r. No complexity bound is claimed.
    """
    value = localized(value)
    if value < CONDUCTOR:
        raise ValueError("the conductor construction requires value >= 5/3")
    if value == CONDUCTOR:
        return PolynomialCertificate(((1, 0, 0), (1, 0, 1)))
    digits = []
    residual = value
    while residual < COARSE_CONDUCTOR:
        digit = residual.numerator % 2
        digits.append(digit)
        residual = (residual - digit) / Q
    return _prepend_digits(digits, _coarse_certificate(residual))


@dataclass(frozen=True)
class MembershipResult:
    """A decision with a polynomial witness or independently checked rejection.

    The cycle rejection relies on the paper's normal-form theorem, as well as
    the exact finite trace. Checking a trace does not replace that theorem.
    """
    is_member: bool
    reason: str
    certificate: PolynomialCertificate | None
    trajectory: tuple[Fraction, ...]

    def verify(self, target) -> bool:
        """Check the supplied evidence without calling decide_membership."""
        try:
            target = exact_rational(target, "target")
            if type(self.is_member) is not bool:
                return False
            if self.is_member:
                return (self.reason == "polynomial"
                        and isinstance(self.certificate, PolynomialCertificate)
                        and self.certificate.verify(target))
            if self.certificate is not None:
                return False
            if self.reason == "outside_localization":
                return not is_localized(target)
            if not isinstance(self.trajectory, tuple) or not self.trajectory:
                return False
            path = tuple(localized(x) for x in self.trajectory)
            if path[0] != target or any(tau(x) != y for x, y in zip(path, path[1:])):
                return False
            if self.reason == "negative_iterate":
                return path[-1] < 0
            if self.reason == "cycle":
                return (all(0 < x < CONDUCTOR for x in path)
                        and path[-1] in path[:-1])
            return False
        except (TypeError, ValueError):
            return False


def decide_membership(value) -> MembershipResult:
    """Decide membership in N_0[2/5,2/3] for an integer or Fraction.

    Iterate tau until a negative value, zero, the conductor, or a repeated
    state is reached. The exponent of 5 in the denominator drops each step
    until zero; the exponent of 3 cannot increase. Any remaining trajectory
    stays in a finite subset of [0,5/3), so this procedure terminates.
    """
    value = exact_rational(value)
    if not is_localized(value):
        return MembershipResult(False, "outside_localization", None, (value,))
    residual = value
    digits = []
    trajectory = []
    seen = set()
    while True:
        trajectory.append(residual)
        if residual < 0:
            return MembershipResult(False, "negative_iterate", None, tuple(trajectory))
        if residual == 0 or residual >= CONDUCTOR:
            terminal = (PolynomialCertificate(()) if residual == 0
                        else conductor_certificate(residual))
            certificate = _prepend_digits(digits, terminal)
            return MembershipResult(True, "polynomial", certificate, tuple(trajectory))
        if residual in seen:
            return MembershipResult(False, "cycle", None, tuple(trajectory))
        seen.add(residual)
        digit = residual.numerator % 2
        digits.append(digit)
        residual = (residual - digit) / Q
