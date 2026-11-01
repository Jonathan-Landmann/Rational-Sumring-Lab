# Rational Sumring Lab

Exact arithmetic, checkable certificates, and complete proofs for rational
semirings. The main [LaTeX paper](paper/main.tex) proves that the multiplicative
monoid of `S = N₀[2/5,2/3]` is **not atomic**: the element `3` has no finite
factorization into atoms. It also classifies the atoms and gives a terminating
exact membership procedure. **IDF remains unresolved**, with a precise reduction
stated below.

This exact non-atomicity conclusion was announced by BakedPotatoz on June 27,
2026 in [CrowdMath progress-log post 7](https://artofproblemsolving.com/polymath/mitprimes2026/f/c4514724h3837652_crowdmath_2026_progress_log).
The paper supplies a complete written argument and credits earlier digit and
perturbation methods. It does **not** claim first discovery or established
novelty of the additional results. This is independent software with no MIT
endorsement; authorship and shared research contributions remain for review.

## Proved results and implemented scope

For `q=2/5`, `r=2/3`, and `h=5/3`, the paper proves:

- The only unit is `1`; `q` is prime, and every nonzero element is uniquely
  `q**k * t` with `v₂(t)=0`.
- Every element of `Z[1/15]` at least `h` belongs to `S`. The threshold is sharp.
- Atoms other than `q` lie in `(1,h]` and have at most one factor of `3` in
  their reduced denominators. A valuation-weight argument then rules out every
  finite atom factorization of `3`.
- All remaining atoms are values of irreducible binary polynomials with constant
  term `1`, or binary prefixes followed by an `r` tail. The paper states and
  proves the exact classification, including infinite atom families tending to `1`.
- Membership in `S` is decidable by exact digit iteration, including a proved
  rejection rule for any nonterminal cycle.

The module `dyadic_semiring.py` implements membership decisions, finite
nonnegative-polynomial witnesses, independently checked rejection traces, and
conductor certificates. It does **not** implement an atom classifier or an IDF
solver. General mathematical conclusions rest on the written proofs, not tests.

The earlier effective-prime work is retained in
[paper/effective_primes_note.tex](paper/effective_primes_note.tex):

| Pair `(q,r)` | Effective primes | Units | One proved atom | Atomicity / IDF in this work |
|---|---|---|---|---|
| `(6/35,19/3)` | `{5,7}` | `{1}` | `6/35` | Not decided |
| `(3/10,7/5)` | `{2,5}` | `{1}` | `3/10` | Not decided |
| `(2/5,2/3)` | `{3,5}` | `{1}` | `2/5` | Non-atomic / IDF unresolved |

Effective-prime decisions and verified witnesses support **all positive rational
pairs**. The official mixed-generator definition is explicitly extended to cover
both generators below one. Novelty of these elementary results is unverified.

## Run

Python 3.10 or later. Runtime code has no third-party dependencies.

```sh
python -m pip install '.[dev]'
rational-sumring-lab --q 6/35 --r 19/3 --degree 2 --coefficients 2 --target 2
rational-sumring-lab --q 3/10 --r 7/5
rational-sumring-lab --q 2/5 --r 2/3
python -m pytest -q
python paper/verify_results.py
python paper/verify_non_atomicity.py
python -m build
```

Without installation, use `python cli.py` with the same arguments. The CLI prints
exact effective primes and certificates. `--exponents 40` adds a bounded witness
search; missing witnesses prove nothing. `--degree` bounds total monomial degree
and `--coefficients` bounds the coefficient sum. `--max-states` caps total distinct
enumerated elements, including zero. It does not bound initial monomial
construction, trial division, or exact exponentiation costs.

### Exact membership in `N₀[2/5,2/3]`

```python
from fractions import Fraction as F
from dyadic_semiring import decide_membership, conductor_certificate

x = F(49, 27)
result = decide_membership(x)
assert result.is_member
assert result.certificate.verify(x)  # evaluates a finite polynomial in 2/5, 2/3
assert result.verify(x)

x = F(27, 25)
result = decide_membership(x)
assert not result.is_member
assert result.reason == "negative_iterate"
assert result.trajectory == (F(27, 25), F(1, 5), F(-2))
assert result.verify(x)

x = F(5, 3) + F(1, 15**30)
assert conductor_certificate(x).verify(x)
```

A `MembershipResult` contains `is_member`, `reason`, `certificate`, and
`trajectory`. Positive answers carry a polynomial certificate. Negative answers
use `negative_iterate`, `cycle`, or `outside_localization`.
`result.verify(x)` checks the supplied evidence without rerunning the decision
procedure. The cycle rejection is justified by the paper's normal-form theorem;
checking a finite trace does not replace that proof. Termination is proved,
but no polynomial-time or bounded-resource claim is made.

### Effective-prime certificates

```python
from fractions import Fraction as F
from certificates import all_certificates

q, r = F(2, 5), F(2, 3)
certificates = all_certificates(q, r)
assert set(certificates) == {3, 5}
assert all(c.verify(q, r) for c in certificates.values())
```

Arithmetic and decision APIs accept integers or `Fraction` values and reject
floats. Certificate coefficients and exponents must be nonnegative integers;
effective-prime certificates require a prime. Malformed certificates return
`False` from `verify`.

## The remaining IDF question

The main paper reduces IDF to the following statement, which is **not proved or
disproved here**: for each fixed positive integer `d` coprime to `30`, only
finitely many nonconstant irreducible binary polynomials `P` in `N₀[X]`, with
`P(0)=1`, satisfy

`5**deg(P) * P(2/5) = d * 3**A` for some nonnegative integer `A`.

The proof shows that atoms with the same numerator part outside `{3,5}` all
divide the single element `3d`. Tail atoms contribute only finitely many atoms
to each such class. Infinite atom families alone therefore do not decide IDF.
Non-atomicity does not imply either IDF or non-IDF.

## Bounded experiments and research status

Sample divisor pairs certify their factors' membership, not irreducibility.
`bounded_factorization_candidates` excludes witnessed reciprocal units, but
other unit statuses may be unknown. Its output can contain reducibles or units
and can omit atoms. `bounded_irreducibles` is a compatibility alias. The absence
of a sampled split does not certify an atom.

The repaired suite currently passes **92 tests**; both independent arithmetic
verification scripts pass. See [the audit](AUDIT.md) for original failures and
exact changes, [the proof guide](PROOF.md), and [paper build instructions](paper/README.md).
The paper is a working draft with disclosed AI assistance. It has not been
submitted to arXiv, human peer reviewed, or checked by a proof assistant.
