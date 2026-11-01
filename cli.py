"""Exact prime certificates and explicitly bounded sumring experiments."""
import argparse
from fractions import Fraction
from certificates import all_certificates
from sumrings import (enumerate_sumring, effective_prime_witnesses,
                      bounded_divisors, bounded_factorization_candidates)


def positive_rational(text):
    try:
        value = Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError("expected a positive rational") from error
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive rational")
    return value


def nonnegative(text):
    try:
        value = int(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected a nonnegative integer") from error
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", required=True, type=positive_rational)
    parser.add_argument("--r", required=True, type=positive_rational)
    parser.add_argument("--degree", type=nonnegative, default=2)
    parser.add_argument("--coefficients", type=nonnegative, default=2)
    parser.add_argument("--exponents", type=nonnegative, default=None,
                        help="optionally compare with a bounded witness search")
    parser.add_argument("--max-states", type=nonnegative, default=200000)
    parser.add_argument("--target", type=positive_rational, default=Fraction(2))
    args = parser.parse_args(argv)
    if args.max_states == 0:
        parser.error("--max-states must be positive")
    print("q =", args.q, "r =", args.r)
    certificates = all_certificates(args.q, args.r)
    print("Effective denominator primes (exact):", sorted(certificates))
    for prime, certificate in certificates.items():
        print(f"  p={prime}: i={certificate.i}, j={certificate.j}, "
              f"q^i*r^j={certificate.monomial}")
    if args.exponents is not None:
        witnesses = effective_prime_witnesses(args.q, args.r, args.exponents)
        print("Primes found within the optional exponent bound:", sorted(witnesses))
    try:
        elements = enumerate_sumring(args.q, args.r, args.degree,
                                     args.coefficients, args.max_states)
    except RuntimeError as error:
        parser.error(str(error))
    print("Enumerated elements:", len(elements))
    print("Sampled divisors of", args.target, ":",
          bounded_divisors(elements, args.target)[:30])
    print("Sample factorization candidates (NOT certified atoms):",
          bounded_factorization_candidates(elements)[:30])
    print("Unit status outside the sample is unknown; candidates can miss atoms.")
    print("Finite enumeration alone does not establish atomicity or IDF.")


if __name__ == "__main__":
    main()
