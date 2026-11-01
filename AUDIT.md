# Repair and mathematical audit — November 1, 2026

## Baseline and reproduced failures

Upstream baseline: `995d8e50213b82bd9215afcf78ce6e9e838d26b2` on `main`.
[Original GitHub run](https://github.com/Jonathan-Landmann/Rational-Sumring-Lab/actions/runs/41350707281).
The Python 3.12 job reported **3 failed, 9 passed**. Local execution reproduced
the same three failures:

| Test | Failure |
|---|---|
| `tests/test_certificates.py::test_named_cases` | `ValueError: require 0 < q < 1 < r` |
| `tests/test_effective_primes.py::test_named_pairs` | Same domain error |
| `tests/test_effective_primes.py::test_finite_witnesses_are_sound` | `ValueError: requires 0 < q < 1 < r and nonnegative bound` |

All three are triggered by `(2/5,2/3)`. The tests' expected set `{3,5}` is
mathematically valid under the natural extended definition; the implementation
omitted that regime. The original CI stopped/cancelled other matrix jobs after
failures, so it did not establish a passing result for any supported version.

An independent baseline package build also failed:
`Multiple top-level modules discovered in a flat-layout: ['effective_primes', 'certificates', 'cli', 'sumrings']`.

The connected GitHub API supplied an immutable source snapshot after direct
Git cloning was unavailable. The local snapshot commit is not the upstream
commit; the GitHub change is based on the upstream SHA above.

## Exact changes

- `effective_primes.py`: positive rational input validation; complete both-below,
  both-above, equality-to-one, and swapped mixed cases; only denominator primes
  are factored and tested.
- `certificates.py`: validates prime, integer exponents, positive exact inputs,
  and monomial equality; malformed certificates return false. Handles either
  generator as a direct witness. Mixed witnesses use a proved terminating
  doubling/binary search in the family `(Bk,Ak+1)`.
- `sumrings.py`: integer square-root primality; rejection of floats, invalid
  primes, zero factorization inputs and invalid budgets; bounded witnesses for
  all positive pairs; incremental total-state cap; explicit sample-unit handling
  and a truthful candidate name with the old name retained as an alias.
- `cli.py`: exact prime set and certificates by default, optional bounded search,
  friendly invalid-input errors, configurable state cap, and clear search limits.
- `pyproject.toml`: explicit build backend/module list, version 0.3.0, installable
  command and build/test extras. `MANIFEST.in` includes proof and paper sources.
- `tests/`: named-case regressions, independent bounded witnesses, strict equality,
  symmetry, generators equal to one, invalid exact inputs, malformed certificates,
  unit-aware sample behavior, budgets, and CLI checks.
- `.github/workflows/tests.yml`: non-fail-fast Python 3.10–3.14 matrix, installed
  package tests, paper arithmetic checker, distribution builds, installed CLI smoke
  test outside the checkout. `.gitignore` excludes generated artifacts.
- `README.md`, `PROOF.md`, `paper/main.tex`, `paper/README.md`: corrected domain,
  complete proofs, reproducible commands, source attribution, and research limits.
- `paper/verify_results.py`: independent integer-divisibility checks of named
  results, proof hypotheses, identities, and explicit rational witness bound.

## Validation

The repaired suite passes **69 tests**. The standalone paper checker passes the
three prime tables and certificates, unit/atom-proof hypotheses, the explicit
reducibility identity, the strict equality boundary, and **848** Bernoulli
constructions over the stated reduced rational grid (largest exponent 36).
Wheel and source-distribution builds and the installed-command smoke test pass.
The paper compiles to a six-page PDF; all pages were rendered and inspected.
The final delivery report records the local interpreter and hosted CI results.

An independent code review also checked 240 bounded polynomial-enumeration
cases against a combinations-with-replacement oracle and 3,025 positive
rational-pair certificate cases using direct denominator arithmetic. These are
finite checks, not general completeness proofs. General correctness rests on
the mathematical arguments in the paper. No proof assistant was used.

## Mathematical status and provenance

The exact official source is [CrowdMath 2026 Open Problem 2](https://artofproblemsolving.com/polymath/mitprimes2026/p/open-prob2),
updated October 15, 2026, and consulted November 1. Its public page data provided
the full statements after a text-only reader could not render the page. All
three requested pairs are present. The title is **Arithmetic Conjectures on
Rational Semirings**. The linked prior chat supplied no accessible attachment.
Requested MathWorks searches did not locate a matching source.

| Claim | Status in this work |
|---|---|
| Mixed effective-prime criterion | Complete elementary proof; already in earlier repository note; novelty unverified |
| Extension to all positive pairs and explicit rational witness bound | Complete proofs; no priority claim |
| Effective primes equal denominator primes of elements below one | Complete proof |
| Units are `{1}` in the three examples | Complete valuation proof |
| Smaller generator is an atom in each example | Complete proof |
| `2/3` is reducible in `N₀[2/5,2/3]` | Exact factorization and proved nonunit factors |
| Non-ACCP and non-atomic-or-non-IDF for the two mixed examples | Prior progress reported by the official project; attributed, not reproved here |
| Atomicity or IDF classification for the named examples/general families | **Not resolved here** |

[Deng–Gotti–Zeng, arXiv:2607.10178](https://arxiv.org/html/2607.10178), Theorem 5.7,
classifies multiplicative finite factorization for one rational generator;
Theorem 5.8 relates BF and ACCP. These are existing results, not this project's
contributions, and cannot be transplanted to two generators without proof.
[Dani–Gotti–Li–Paladiya, arXiv:2609.32138](https://arxiv.org/html/2609.32138),
introductory footnote 1, announces forthcoming non-atomic rational examples by
Cen et al. A complete public proof was not located in this audit, so the
announcement is not treated as a verified theorem or an answer to the distinct
existence-of-atomic-examples question. The [Abedi et al. manuscript](https://math.mit.edu/research/highschool/primes/materials/2025/CMI-2.pdf)
studies **additive** monoids; its FF/BF/ACCP results are not multiplicative answers.

The paper is a working preprint-style draft with disclosed AI assistance and
author attribution pending review. No novel-discovery claim, arXiv submission,
or resolution of the atomicity/IDF questions has been made. The published
discussion was not exhaustively searched for priority; author/mentor review is
needed before claiming new mathematics or submitting the paper.
