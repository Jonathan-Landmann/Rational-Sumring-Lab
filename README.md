# Rational Sumring Lab

Exact arithmetic and checkable certificates for positive rational semirings
`N₀[q,r]`. Inspired by [CrowdMath 2026: Arithmetic Conjectures on Rational
Semirings](https://artofproblemsolving.com/polymath/mitprimes2026), especially
[Open Problem 2](https://artofproblemsolving.com/polymath/mitprimes2026/p/open-prob2).
Independent software; no MIT endorsement or open-problem resolution is claimed.

## Verified scope

- Exact effective-denominator-prime decisions for **all positive rational pairs**.
- Constructive witnesses checked from their defining inequalities using exact arithmetic.
- Bounded semiring enumeration and divisor witnesses with explicit limits.
- A [LaTeX research note](paper/main.tex) proving the criterion, a rational witness
  bound, equivalence with denominators of elements below one, and a unit obstruction.
- Complete elementary proofs that all three examples have only the unit `1` and
  that their smaller generator is an atom. These do **not** prove atomicity or IDF.

| Pair `(q,r)` | Effective primes | Units | One proved atom |
|---|---|---|---|
| `(6/35,19/3)` | `{5,7}` | `{1}` | `6/35` |
| `(3/10,7/5)` | `{2,5}` | `{1}` | `3/10` |
| `(2/5,2/3)` | `{3,5}` | `{1}` | `2/5` |

The official effective-prime definition assumes `0<q<1<r`; the third row uses
our explicit extension to arbitrary positive pairs. Novelty of these elementary
proofs is **unverified**. The paper distinguishes known literature, reported
project progress, and results proved here.

## Run

Python 3.10 or later. Runtime code has no third-party dependencies.

```sh
python -m pip install '.[dev]'
rational-sumring-lab --q 6/35 --r 19/3 --degree 2 --coefficients 2 --target 2
rational-sumring-lab --q 3/10 --r 7/5
rational-sumring-lab --q 2/5 --r 2/3
python -m pytest -q
python paper/verify_results.py
python -m build
```

Without installation, use `python cli.py` with the same arguments. The CLI prints
the exact prime set and certificates by default. `--exponents 40` additionally
runs a bounded comparison search; missing witnesses prove nothing.
`--degree` bounds total monomial degree; `--coefficients` bounds the coefficient
sum. `--max-states` caps total distinct enumerated elements, including zero,
and raises an error when exceeded. It does not bound initial monomial generation,
trial division, or exact exponentiation costs.

```python
from fractions import Fraction
from certificates import all_certificates

q, r = Fraction(2, 5), Fraction(2, 3)
certificates = all_certificates(q, r)
assert set(certificates) == {3, 5}
assert all(c.verify(q, r) for c in certificates.values())
```

Numerical API inputs must be `int` or `Fraction`; floats are rejected.
Certificate exponents must be nonnegative integers and the base must be prime.
Malformed certificates return `False` from `verify`.

## Research limitations

The multiplicative atomicity and IDF questions remain unresolved by this work.
Sample divisor pairs certify their factors' membership, not irreducibility.
`bounded_factorization_candidates` excludes units whose reciprocals occur in
the sample, but other unit statuses can be unknown. Its output can contain
reducibles or units and can omit atoms. `bounded_irreducibles` is a compatibility
alias. Once trivial units have been proved independently, a split with both
factors unequal to one certifies reducibility; absence of a sampled split still
does not certify an atom.

See [PROOF.md](PROOF.md), [paper build instructions](paper/README.md), and
[the audit of failures and changes](AUDIT.md). The paper is a working draft for
author and mathematical review, not an arXiv submission or a novelty claim.

