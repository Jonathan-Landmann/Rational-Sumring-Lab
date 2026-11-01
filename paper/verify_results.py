"""Reproduce the paper's finite exact checks using only the standard library.

Run ``python paper/verify_results.py`` from the repository root.  The arithmetic
below is independent of the implementation's valuation and witness routines.
These finite checks supplement, and do not replace, the proofs in main.tex.
"""

from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from certificates import all_certificates
from effective_primes import effective_primes_exact


def require(condition, message):
    """Keep verification enabled even when Python is run with -O."""
    if not condition:
        raise AssertionError(message)


def p_order(value, prime):
    """Direct integer divisibility calculation for positive rational values."""
    numerator, denominator = value.numerator, value.denominator
    order = 0
    while numerator % prime == 0:
        numerator //= prime
        order += 1
    while denominator % prime == 0:
        denominator //= prime
        order -= 1
    return order


def bernoulli_witness(q, r, prime):
    """The paper's explicit construction in the mixed, nontrivial case."""
    a, b = p_order(q, prime), -p_order(r, prime)
    require(0 < q < 1 < r and a >= 0 and b > 0, "construction hypotheses")
    t = q**b * r**a
    require(t < 1, "strict effectiveness inequality")
    threshold = (r - 1) * t / (1 - t)
    k = threshold.numerator // threshold.denominator + 1
    i, j = b * k, a * k + 1
    value = q**i * r**j
    require(0 < value < 1, "constructed monomial is below one")
    require(p_order(value, prime) == -b, "constructed valuation is -B")
    return i, j, value


def check_named_examples():
    f = Fraction
    # All denominator primes are explicitly included in each support tuple.
    examples = (
        (f(6, 35), f(19, 3), (3, 5, 7), {5, 7}, 2),
        (f(3, 10), f(7, 5), (2, 5), {2, 5}, 3),
        (f(2, 5), f(2, 3), (3, 5), {3, 5}, 2),
    )
    for q, r, support, expected, obstruction_prime in examples:
        # Independently evaluate the finite criterion for the table.  The
        # negative answer for p=3 in the first row is certified by t>=1;
        # positive answers have directly checkable monomial certificates.
        classified = set()
        for prime in support:
            a, c = p_order(q, prime), p_order(r, prime)
            if q < 1 and a < 0 or r < 1 and c < 0:
                classified.add(prime)
            elif q < 1 < r and a >= 0 and c < 0:
                if q**(-c) * r**a < 1:
                    classified.add(prime)
        require(classified == expected, "independent named table classification")
        require(effective_primes_exact(q, r) == expected, "public classification")
        certificates = all_certificates(q, r)
        require(set(certificates) == expected, "named certificate prime set")
        for prime, certificate in certificates.items():
            require(type(certificate.i) is int and type(certificate.j) is int,
                    "certificate exponents are integers")
            require(certificate.i >= 0 and certificate.j >= 0,
                    "certificate exponents are nonnegative")
            value = q**certificate.i * r**certificate.j
            require(value == certificate.monomial and 0 < value < 1,
                    "independent certificate value check")
            require(p_order(value, prime) < 0, "independent certificate valuation")
        # Verify the finite hypotheses of the paper's trivial-unit lemma.
        # The general lemma, rather than finite enumeration, proves S^x={1}.
        for generator in (q, r):
            order = p_order(generator, obstruction_prime)
            require(order >= 0, "unit obstruction: nonnegative generator order")
            require(generator >= 1 or order > 0,
                    "unit obstruction: positive order below one")
        # These finite hypotheses feed the paper's proof that q is an atom.
        # Checking them is not an enumeration-based irreducibility proof.
        require(0 < q < 1 and p_order(q, obstruction_prime) == 1,
                "specified atom: q is below one and has valuation one")
        if r > 1:
            require(p_order(r, obstruction_prime) == 0,
                    "specified atom: mixed companion has valuation zero")
        else:
            require(q <= r < 1 and p_order(r, obstruction_prime) == 1,
                    "specified atom: q is the smaller valuation-one generator")


def check_reducibility_identity():
    q, r = Fraction(2, 5), Fraction(2, 3)
    companion = 1 + r  # Explicit semiring membership as a nonnegative sum.
    require(q * companion == r, "exact reducibility identity for 2/3")
    require(q != 1 and companion != 1, "both displayed factors differ from one")
    # The proved trivial-unit result, not this calculation alone, establishes
    # that the two factors are nonunits.


def check_boundaries():
    q, r = Fraction(2, 3), Fraction(3, 2)
    a, b = p_order(q, 2), -p_order(r, 2)
    require(a == b == 1 and q**b * r**a == 1, "equality boundary for p=2")
    require(effective_primes_exact(q, r) == {3}, "boundary rejects p=2")
    q, r = Fraction(4, 5), Fraction(11, 8)
    require(q**3 * r**2 == Fraction(121, 125), "near-boundary exact value")
    i, j, value = bernoulli_witness(q, r, 2)
    require((i, j) == (36, 25), "explicit near-boundary exponents")
    require(p_order(value, 2) == -3, "near-boundary valuation")


def check_bernoulli_grid():
    below_one = sorted({Fraction(a, b) for b in range(2, 12)
                        for a in range(1, b)})
    above_one = sorted({Fraction(c, d) for c in range(2, 12)
                        for d in range(1, c)})
    count = 0
    largest_exponent = 0
    for q in below_one:
        for r in above_one:
            for prime in (2, 3, 5, 7, 11):
                a, c = p_order(q, prime), p_order(r, prime)
                if a >= 0 and c < 0 and q**(-c) * r**a < 1:
                    i, j, _ = bernoulli_witness(q, r, prime)
                    require(prime in effective_primes_exact(q, r),
                            "public criterion includes independently witnessed prime")
                    count += 1
                    largest_exponent = max(largest_exponent, i, j)
    require(count == 848, "reproducible grid size")
    require(largest_exponent == 36, "reproducible largest constructed exponent")
    return count, largest_exponent


def main():
    check_named_examples()
    check_reducibility_identity()
    check_boundaries()
    count, largest_exponent = check_bernoulli_grid()
    print("PASS: all three named effective-prime tables and certificates.")
    print("PASS: the trivial-unit lemma's hypotheses for all three named pairs.")
    print("PASS: specified-atom proof hypotheses and exact reducibility identity.")
    print("PASS: strict equality boundary and explicit near-boundary certificate.")
    print(f"PASS: {count} Bernoulli constructions; largest exponent {largest_exponent}.")
    print("These are exhaustive checks of the stated finite grid, not proofs of")
    print("the general theorems, atomicity, or IDF. See main.tex for proofs and scope.")


if __name__ == "__main__":
    main()
