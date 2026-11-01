# Papers and exact verification

[main.tex](main.tex) is the main self-contained LaTeX working draft. It proves
that `3` has no finite atom factorization in the multiplicative monoid of
`N₀[2/5,2/3]`, hence that this monoid is not atomic. It also proves a sharp
conductor `5/3`, a complete atom classification, and a terminating exact
membership procedure. **IDF is not decided**: it is reduced to a stated
finiteness question for irreducible binary polynomials with specified numerator
parts.

The exact non-atomicity conclusion was announced by BakedPotatoz on June 27,
2026 in [CrowdMath progress-log post 7](https://artofproblemsolving.com/polymath/mitprimes2026/f/c4514724h3837652_crowdmath_2026_progress_log).
The paper supplies a complete written proof and attributes earlier digit and
perturbation methods. It does not claim first discovery or established priority
for the additional results.

[effective_primes_note.tex](effective_primes_note.tex) retains the earlier
standalone note: the exact effective-prime criterion, its extension to all
positive rational pairs, a rational witness bound, and elementary unit and
specified-atom results for all three requested examples. Those results do not
classify atomicity or IDF for the two mixed-generator examples.

Both sources have embedded bibliographies and no external figures. They have
not been submitted to arXiv. Authorship remains for review, and AI assistance
is disclosed.

## Build and verify

From the repository root:

```sh
python -m pytest -q
python paper/verify_results.py
python paper/verify_non_atomicity.py
tectonic --keep-logs --outdir paper paper/main.tex
tectonic --keep-logs --outdir paper paper/effective_primes_note.tex
```

Alternatively run `pdflatex main.tex` twice, and
`pdflatex effective_primes_note.tex` twice, from the `paper` directory.

The verification scripts use only the Python standard library:

- `verify_results.py` independently checks the three effective-prime tables,
  certificate values, unit/atom-proof hypotheses, an explicit factorization,
  boundary cases, and **848** Bernoulli constructions.
- `verify_non_atomicity.py` checks **425** conductor certificates and two
  high-denominator examples, **17** sharp-boundary obstructions, the exclusion
  of `27/25`, **60** digit identities, **30** explicit monomial remainder
  certificates, **16** finite atom-family identities, **233** independently
  constructed polynomial members, and **833** exact membership decisions with
  checked evidence (**512** positive and **321** negative).

The suite currently passes **92 tests**. These are finite computational checks;
the general non-atomicity, classification, and membership theorems are proved
in the text. No proof assistant was used, and successful compilation does not
establish mathematical validity or arXiv acceptance.

The original problem source is [CrowdMath Open Problem 2](https://artofproblemsolving.com/polymath/mitprimes2026/p/open-prob2),
consulted November 1, 2026. The linked prior chat had no accessible attachment;
the complete official online problem was recovered and used instead.

Before submission, a human author must review the mathematics, authorship,
literature priority, and attribution of shared CrowdMath contributions.
