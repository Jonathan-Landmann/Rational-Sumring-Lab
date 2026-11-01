# Proof guide and mathematical scope

The complete argument for `S=N₀[2/5,2/3]` is in [paper/main.tex](paper/main.tex).
It proves non-atomicity, with the explicit witness `3`, and gives an atom
classification and exact membership procedure. **It does not decide IDF.**
The earlier general effective-prime proofs are preserved in
[paper/effective_primes_note.tex](paper/effective_primes_note.tex) and summarized
below.

## Non-atomicity of `N₀[2/5,2/3]`

Set `q=2/5`, `r=2/3`, `h=5/3`, and `R=Z[1/15]`. The proof uses these steps:

1. `r=q+qr` and `r/q=1+r`. With `epsilon(x)` the residue in `{0,1}` modulo
   `2R`, the map `tau(x)=(x-epsilon(x))/q` preserves `S`. Its backward
   implication also holds: `tau(x) in S` implies `x in S`.
2. Every element of valuation zero at `2` is at least `1`. Consequently the
   units are `{1}`, `q` is prime, and each nonzero element is uniquely `q**k*t`
   with `v₂(t)=0`. The only atom of positive `2`-valuation is `q`.
3. CRT residue expansions first prove that every element of `R` at least
   `20/3` belongs to `S`. For `x>h`,
   `tau(x)-h >= (5/2)*(x-h)`, so iteration and the backward implication lower
   the threshold to `h`. It is sharp: `h-2*q**n` tends to `h` from below but
   its `n`th iterate is `-1/3`, ruling out membership.
4. Technical fractions `3**a*5**b` belonging to `S` occur arbitrarily near
   `1` from above, while satisfying any prescribed congruence to `1` modulo
   a power of `2`. The proof combines density of the logarithmic subgroup,
   an exact congruence, and the conductor theorem.
5. If an atom other than `q` had an iterate above `h`, such a technical
   fraction could divide it into two nonunits. Thus all its iterates lie in
   `[0,h]`. An expression `x=2*q**n+z`, `z in S`, would instead give
   `tau**n(x)=2+tau**n(z)>h`, and is impossible.
6. Expanding `r=q(1+r)` shows that any monomial with `r`-degree at least two,
   or any two linear `r` terms, produces a forbidden `2*q**n` summand.
   Therefore an atom other than `q` lies in `(1,h]` and has reduced
   denominator exponent at most one at `3`.
7. Any atoms in a hypothetical factorization of `3` must be technical.
   Under the preceding restrictions, such an atom is either `h`, of weight
   `delta=v₃+v₅=0`, or `3**A/5**B` with `A>B>=1`. Weight one allows only
   `27/25` inside `(1,h]`; however `tau(27/25)=1/5` and `tau**2(27/25)=-2`,
   so it is not in `S`. Every technical atom therefore has weight zero or
   at least two. Their weights cannot sum to `delta(3)=1`.

This excludes products of **every finite length**. It is not an inference from
bounded factor searches. The paper supplies all arguments, including the
technical-fraction perturbation and the denominator restriction.

## Atom classification and total membership

An element of `S` has all its digit iterates in `[0,h]` exactly when it is a
finite binary polynomial `P(q)` or a binary prefix `P(q)+q**n*r` with
`deg(P)<=n`. This normal-form statement includes zero and does not itself
assert atomhood.

The atoms are exactly:

- `q`;
- `P(q)` for a nonconstant binary polynomial with `P(0)=1` irreducible in
  the polynomial semiring `N₀[X]`;
- `P(q)+q**n*r` with binary `P`, `P(0)=1`, and `deg(P)<=n`.

Binary evaluation is injective because `q<1/2`. The classification proof checks
that any forbidden product creates a `2*q**n` summand. It proves, in particular,
that `h`, `1+q**n` (`n>=1`), and `1+q**n*r` (`n>=0`) are atoms.

For exact membership, reject rationals outside `R`; otherwise iterate `tau`.
Accept at zero or at least `h`, and reject at a negative iterate or a repeated
nonterminal state. A member with bounded iterates has the normal forms above,
which eventually reach zero or `h`, so it cannot enter such a cycle.
Termination follows because the denominator's `5` exponent decreases until
zero and its `3` exponent cannot increase; the remaining bounded orbit lies in
a finite lattice. This argument does not assume that nonterminal cycles are
absent. `dyadic_semiring.decide_membership` implements the procedure with
independently checkable positive certificates or rejection evidence.

## IDF remains unresolved

For an atom other than `q`, let `d` be its numerator part supported outside
`{3,5}`. It is coprime to `30`. All atoms with this same `d` divide `3d`, by
the conductor theorem. Conversely only finitely many such `d` can occur among
atom divisors of a fixed element. Tail atoms contribute finitely many atoms
for each fixed `d`.

Thus IDF is equivalent to finiteness, for every fixed positive `d` coprime to
`30`, of the nonconstant irreducible binary polynomials `P` with `P(0)=1`
satisfying

`5**deg(P) * P(2/5) = d * 3**A`, for some `A>=0`.

No proof or counterexample to this finiteness statement is supplied. The other
two named rational pairs and general families are not classified here.

## General effective-prime criterion

All parameters in this section are positive rationals and valuations are at
primes. For mixed generators `0<q<1<r`, set `A=v_p(q)` and `C=v_p(r)`.
A prime is effective exactly when

`A < 0`, or `A >= 0`, `C < 0`, and `q**(-C) * r**A < 1`.

If `A<0`, use `q`. If `A,C>=0`, no monomial has negative valuation.
Otherwise put `B=-C>0`, `t=q**B*r**A`. For a witness `m=q**i*r**j`,
one has `i>0` and `Bj-Ai>0`. If `t>=1`, then
`m**B=t**i*r**(Bj-Ai)>1`, a contradiction. Thus `t<1` is necessary.

For sufficiency set `K=floor((r-1)*t/(1-t))+1`, `i=B*K`, `j=A*K+1`.
With `delta=(1-t)/t`, the binomial theorem gives
`t**(-K)=(1+delta)**K >= 1+K*delta > r`.
Thus `q**i*r**j=r*t**K<1` and its valuation is `-B<0`.

This gives a rational termination bound. The implementation uses doubling and
binary search for the least positive `k` in this family. It does not claim a
globally smallest exponent pair or polynomial bit complexity. The strict
inequality excludes `t=1`.

For every positive pair:

- Both generators at least one: the effective-prime set is empty.
- Both generators at most one: it is their denominator-prime union.
- Generators straddling one: reorder and apply the mixed criterion.
- A generator equal to one is covered by the first two cases.

Primes outside the denominator supports have nonnegative monomial valuations.
These cases explicitly extend the official mixed-generator definition.

Effectiveness is also equivalent to a denominator prime appearing in an element
`0<x<1`. In a positive polynomial sum every term is at most `x`, and negative
valuation of the sum forces a term with negative valuation. Positive integer
coefficients cannot introduce a negative valuation. Powers of a witness give
arbitrarily negative valuations arbitrarily near zero.

The companion note proves a valuation obstruction to nontrivial units and
applies it to `(6/35,19/3)`, `(3/10,7/5)`, and `(2/5,2/3)`, using the primes
`2,3,2`, respectively. It also proves that the smaller generator is an atom
in each pair. In the third example `r` is reducible because `r=q*(1+r)`.
These elementary results remain available independently of the main paper.

## Provenance and verification

BakedPotatoz announced non-atomicity of this exact semiring on June 27, 2026 in
[CrowdMath progress-log post 7](https://artofproblemsolving.com/polymath/mitprimes2026/f/c4514724h3837652_crowdmath_2026_progress_log),
without writing out the proof there. The main paper provides a complete
argument and credits earlier project digit and perturbation methods. It makes
no first-discovery claim. Priority of the additional results and the earlier
effective-prime proofs is unestablished.

The written proofs and exact computations have been reviewed by independent
agents, not human peer reviewers or a proof assistant. The paper discloses AI
assistance; authorship, priority, and attribution require review before any
submission. Finite checks support the written proofs and do not establish the
general conclusions by themselves.
