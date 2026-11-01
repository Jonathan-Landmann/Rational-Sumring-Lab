import argparse
from fractions import Fraction
from sumrings import (enumerate_sumring, effective_prime_witnesses,
                      bounded_divisors, bounded_irreducibles)

def main():
    p = argparse.ArgumentParser(description="Bounded rational sumring experiments")
    p.add_argument("--q", required=True, type=Fraction)
    p.add_argument("--r", required=True, type=Fraction)
    p.add_argument("--degree", type=int, default=2)
    p.add_argument("--coefficients", type=int, default=2)
    p.add_argument("--exponents", type=int, default=30)
    p.add_argument("--target", type=Fraction, default=Fraction(2))
    a = p.parse_args()
    print("q =", a.q, "r =", a.r)
    if 0 < a.q < 1 < a.r:
        witnesses = effective_prime_witnesses(a.q, a.r, a.exponents)
        print("Effective denominator primes witnessed (not exhaustive):")
        for prime, (i, j, x) in sorted(witnesses.items()):
            print(f"  p={prime}: i={i}, j={j}, q^i*r^j={x}")
    els = enumerate_sumring(a.q, a.r, a.degree, a.coefficients)
    print("Enumerated elements:", len(els))
    print("Sampled divisors of", a.target, ":", bounded_divisors(els, a.target)[:30])
    print("Bounded irreducibility candidates (NOT certified atoms):",
          bounded_irreducibles(els)[:30])
    print("WARNING: Finite enumeration cannot establish atomicity or IDF.")

if __name__ == "__main__":
    main()
