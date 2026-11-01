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
- `certificates.py`: validates the prime, integer exponents, positive exact
  inputs, and monomial equality; malformed certificates return false. Either
  generator can supply a direct witness. Mixed witnesses use a proved
  terminating doubling/binary search in the family `(Bk,Ak+1)`.
- `sumrings.py`: integer square-root primality; rejection of floats, invalid
  primes, zero factorization inputs, and invalid budgets; bounded witnesses for
  all positive pairs; incremental total-state cap; explicit sample-unit handling
  and a truthful candidate name with the old name retained as an alias.
- `cli.py`: exact prime sets and certificates by default, optional bounded
  search, invalid-input errors, configurable state cap, and explicit search
  limits. The new semiring membership procedure is a Python API, not a new CLI
  command.
- `dyadic_semiring.py`: exact domain and parity checks for `Z[1/15]`, the digit
  map `tau`, binary prefixes, and `PolynomialCertificate`. The conductor
  construction combines finite CRT residue expansions with digit reduction.
  `decide_membership` implements the proved terminating procedure and returns
  `MembershipResult` with a polynomial witness or a domain/negative-iterate/cycle
  rejection. `MembershipResult.verify` checks evidence without invoking the
  decision procedure; cycle rejection relies on the written normal-form theorem.
- `pyproject.toml`: explicit build backend and module list, release metadata,
  installable command, and build/test extras. `MANIFEST.in` includes proof and
  paper sources.
- `tests/`: named-case regressions, independent bounded witnesses, strict
  equality, symmetry, generators equal to one, exact-input validation, malformed
  certificates, unit-aware sample behavior, budgets, and CLI checks. New semiring
  tests cover conductor witnesses, high denominators, sharp boundary
  obstructions, digit identities, independently constructed polynomial members,
  total membership evidence, and rejection of tampered evidence.
- `.github/workflows/tests.yml`: non-fail-fast Python 3.10–3.14 matrix, installed
  package tests, both arithmetic verification scripts, distribution builds, and
  installed CLI smoke testing outside the checkout. `.gitignore` excludes
  generated artifacts.
- `paper/main.tex`: complete non-atomicity proof with witness `3`, atom
  classification, sharp conductor, exact membership algorithm, and a precise
  unresolved IDF reduction, with provenance and AI-assistance disclosure.
- `paper/effective_primes_note.tex`: retains the earlier effective-prime,
  unit, and specified-atom proofs for all three examples.
- `paper/verify_results.py`: independent integer-divisibility checks of the
  earlier named results, hypotheses, identities, and explicit witness bound.
- `paper/verify_non_atomicity.py`: finite exact checks of conductor certificates,
  digit and remainder identities, the excluded weight-one candidate, atom-family
  identities, and membership decisions. It explicitly distinguishes these
  checks from the general written proofs.
- `README.md`, `PROOF.md`, and `paper/README.md`: current mathematical scope,
  exact membership usage, reproducible commands, prior announcements, and limits.

## Validation

The current suite passes **92 tests** on each of local Python 3.12.14 and
3.14.7. Both standalone verification scripts pass. The main paper compiles
without warnings to eight pages; every page was rendered and visually inspected.

The earlier checker verifies the three prime tables and certificates,
unit/atom-proof hypotheses, the explicit reducibility identity, the strict
boundary, and **848** Bernoulli constructions (largest exponent 36).

The new checker verifies **425** conductor certificates and two high-denominator
examples; **17** sharp-boundary obstructions; exact nonmembership of `27/25`;
**60** double-summand digit identities; **30** explicit nonnegative remainder
certificates for high `r`-degree monomials; **16** finite atom-family identities;
**233** independently constructed polynomial members; and **833** membership
parameter cases with checked evidence (**512** positive, **321** negative).
It does not infer the absence of nonterminal cycles from this finite grid.

Version 0.4.0 wheel and source-distribution builds, installation, and smoke
checks outside the checkout pass, including imports and membership calls from
the installed package.
The final delivery report records the local interpreter, rendered paper review,
and hosted CI results separately; a configured CI matrix is not itself evidence
that every hosted job passed.

An independent code review also checked 240 bounded polynomial-enumeration
cases against a combinations-with-replacement oracle and 3,025 positive
rational-pair certificate cases using direct denominator arithmetic. These are
finite checks, not general completeness proofs. General correctness and the
non-atomicity conclusion rest on the mathematical arguments. No proof assistant
was used.

## Mathematical status and provenance

The exact official source is [CrowdMath 2026 Open Problem 2](https://artofproblemsolving.com/polymath/mitprimes2026/p/open-prob2),
updated October 15, 2026, and consulted November 1. Its public page data provided
the full statements after a text-only reader could not render the page. All
three requested pairs are present. The title is **Arithmetic Conjectures on
Rational Semirings**. The linked prior chat supplied no accessible attachment.
Requested MathWorks searches did not locate a matching source.

The exact conclusion that `N₀[2/5,2/3]` is not atomic was announced by
**BakedPotatoz on June 27, 2026**, in
[CrowdMath progress-log post 7](https://artofproblemsolving.com/polymath/mitprimes2026/f/c4514724h3837652_crowdmath_2026_progress_log),
with the proof left unwritten there. Therefore this work makes **no
first-discovery claim**. Earlier project writeups develop digit expansions,
valuation bounds, and technical-fraction perturbations near one; the main paper
credits those methods and supplies all arguments needed for the present result.
A complete earlier proof of this exact conclusion was not located in the
limited audit, which does not establish priority. Novelty of the atom
classification, conductor, membership procedure, and IDF reduction is likewise
not established.

| Claim | Status in this work |
|---|---|
| Mixed effective-prime criterion | Complete elementary proof; already in the earlier repository note; novelty unverified |
| All-positive-pair extension and rational witness bound | Complete proofs; no priority claim |
| Effectiveness equals denominator occurrence below one | Complete proof |
| Units are `{1}` and smaller generator is an atom in the three examples | Complete valuation proofs |
| `2/3` is reducible in `N₀[2/5,2/3]` | Exact factorization with proved nonunit factors |
| `3` has no finite atom factorization in `N₀[2/5,2/3]` | Complete proof; the non-atomicity conclusion was announced previously |
| Sharp conductor `5/3`, atom classification, and exact membership for this semiring | Complete proofs and supporting exact code; priority unestablished |
| IDF for `N₀[2/5,2/3]` | **Unresolved**; reduced to an explicit binary-polynomial finiteness question |
| Atomicity/IDF of the other two examples and general families | **Not decided by this work** |

For the remaining IDF question, the proved equivalence is: for each fixed
positive integer `d` coprime to `30`, there are only finitely many nonconstant
irreducible binary polynomials `P` in `N₀[X]`, with `P(0)=1`, satisfying
`5**deg(P) * P(2/5) = d * 3**A` for some `A>=0`. The equivalence is proved;
the finiteness assertion is not. Infinite atom families alone do not answer it.

[Deng–Gotti–Zeng, arXiv:2607.10178](https://arxiv.org/html/2607.10178), Theorem 5.7,
classifies multiplicative finite factorization for one rational generator;
Theorem 5.8 relates BF and ACCP. These are existing results, not this project's
contributions, and cannot be transplanted to two generators without proof.
[Dani–Gotti–Li–Paladiya, arXiv:2609.32138](https://arxiv.org/html/2609.32138),
introductory footnote 1, announces forthcoming non-atomic rational examples by
Cen et al. That separate announcement is not substituted for the self-contained
proof here, nor treated as an answer to the existence-of-atomic-examples
question. The [Abedi et al. manuscript](https://math.mit.edu/research/highschool/primes/materials/2025/CMI-2.pdf)
studies **additive** monoids; its FF/BF/ACCP results are not multiplicative answers.

The papers are working preprint-style drafts with disclosed AI assistance and
author attribution pending review. Their arguments received independent agent
review, not human peer review or proof-assistant verification. No arXiv
submission or established novelty is claimed. The discussion was not
exhaustively searched for priority; human author/mentor review is needed before
claiming new mathematics or submitting the papers.
