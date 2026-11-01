"""Exact bounded experiments for N_0[q,r]; negative searches prove nothing."""
from fractions import Fraction
from math import isqrt


def rational(s: str) -> Fraction:
    """Parse an explicitly supplied rational string without floating point."""
    return Fraction(s)


def exact_rational(value, name: str = "value") -> Fraction:
    """Accept integers/Fractions only; do not silently import float rounding."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def positive_pair(q, r) -> tuple[Fraction, Fraction]:
    q, r = exact_rational(q, "q"), exact_rational(r, "r")
    if q <= 0 or r <= 0:
        raise ValueError("q and r must be positive")
    return q, r


def nonnegative_integer(value, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def is_prime(p: int) -> bool:
    """Trial division with an integer square-root bound (no float rounding)."""
    if isinstance(p, bool) or not isinstance(p, int) or p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    return all(p % d for d in range(3, isqrt(p) + 1, 2))


def generators(q: Fraction, r: Fraction, degree: int) -> list[Fraction]:
    q, r = positive_pair(q, r)
    nonnegative_integer(degree, "degree")
    return sorted({q**i * r**j for i in range(degree + 1)
                   for j in range(degree + 1 - i)})


def enumerate_sumring(q: Fraction, r: Fraction, degree: int = 3,
                      coefficient_sum: int = 3, max_states: int = 200000):
    """Enumerate bounded sums; max_states caps the total distinct output states.

    The cap is checked on insertion, before a complete oversized layer is built.
    It does not bound the cost of generating the initial monomials.
    """
    q, r = positive_pair(q, r)
    nonnegative_integer(degree, "degree")
    nonnegative_integer(coefficient_sum, "coefficient_sum")
    nonnegative_integer(max_states, "max_states")
    if max_states == 0:
        raise ValueError("max_states must be positive")
    if coefficient_sum == 0:
        return {Fraction(0)}
    gs = generators(q, r, degree)
    frontier = {Fraction(0)}
    seen = set(frontier)
    for _ in range(coefficient_sum):
        next_layer = set()
        for v in frontier:
            for g in gs:
                x = v + g
                if x not in seen:
                    if len(seen) >= max_states:
                        raise RuntimeError("state limit exceeded; reduce search bounds")
                    seen.add(x)
                next_layer.add(x)
        frontier = next_layer
    return seen


def valuation(x: Fraction, p: int) -> int:
    x = exact_rational(x)
    if not is_prime(p):
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


def prime_factors(n: int) -> list[int]:
    """Distinct prime factors of a nonzero integer; 1 has no prime factors."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n == 0:
        raise ValueError("zero has no finite prime factorization")
    n = abs(n)
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        ans.append(n)
    return ans


def effective_prime_witnesses(q: Fraction, r: Fraction, exponent_bound: int = 40):
    """Find bounded witnesses for any positive pair; absence proves nothing."""
    q, r = positive_pair(q, r)
    nonnegative_integer(exponent_bound, "exponent_bound")
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
    """Return exact witnessed divisor pairs in a nonnegative rational sample."""
    target = exact_rational(target, "target")
    if target <= 0:
        raise ValueError("target must be positive")
    elements = {exact_rational(x) for x in elements}
    if any(x < 0 for x in elements):
        raise ValueError("sample elements must be nonnegative")
    return sorted((d, target / d) for d in elements
                  if d != 0 and target / d in elements)


def bounded_factorization_candidates(elements):
    """Sample-based candidates, with witnessed units excluded.

    A reciprocal in the sample proves an element is a unit. Other elements
    need not be nonunits. A split using two elements whose unit status is
    unknown is only a sample split: excluded elements can still be atoms, and
    returned elements can still be units or reducible in the full monoid.
    """
    elements = {exact_rational(x) for x in elements}
    if any(x < 0 for x in elements):
        raise ValueError("sample elements must be nonnegative")
    positive = sorted(x for x in elements if x > 0)
    units = {x for x in positive if x == 1 or 1 / x in elements}
    candidates = [x for x in positive if x not in units]
    return [x for x in candidates if not any(
        x / a in elements and x / a not in units for a in candidates)]


def bounded_irreducibles(elements):
    """Compatibility alias; these are NOT certified atoms or all possible atoms."""
    return bounded_factorization_candidates(elements)
