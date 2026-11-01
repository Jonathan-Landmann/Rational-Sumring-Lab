# Rational Sumring Lab

Independent computational exploration of **Arithmetic Conjectures on Rational Sumrings**, inspired by the 2026 MIT PRIMES CrowdMath problem statement. This is not an official MIT repository and does not claim to resolve an open problem.

For rational q and r, N₀[q,r] consists of finite sums of nonnegative integer multiples of q^i r^j. Its nonzero elements form a multiplicative monoid.

## Features
- Exact rational arithmetic via Python's fractions.Fraction
- Bounded enumeration of sumring elements
- Prime-adic valuations and verifiable witnesses for effective denominator primes
- Finite divisor searches and tentative irreducibility candidates
- Automated tests and a command-line interface

## Run

Python 3.10+; pytest is needed only for tests.

```bash
python cli.py --q 6/35 --r 19/3 --degree 2 --coefficients 2 --exponents 40 --target 2
python cli.py --q 3/10 --r 7/5
python cli.py --q 2/5 --r 2/3
python -m pytest -q
```

## Scientific limitations

Finite computation **cannot prove** atomicity, non-atomicity, IDF, or non-IDF for an infinite monoid. Missing witnesses are not evidence of nonexistence. Candidates without factorizations in a finite sample are not certified atoms. Units and associate classes of the full monoid must be characterized independently.

Future work: valuation-based witness bounds, rigorous units and associate-class analysis, symbolic families of divisors, and reproducible experiments for the specified rational pairs.

Independent experimental software; no MIT endorsement or mathematical discovery is asserted.
