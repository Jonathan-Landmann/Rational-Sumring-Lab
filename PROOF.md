# Exact effectiveness criterion and proof scope

Full definitions, proofs, and references appear in [paper/main.tex](paper/main.tex).
All parameters below are positive rationals and valuations are at primes.

## Mixed generators: 0 < q < 1 < r

Set `A=v_p(q)` and `C=v_p(r)`. A prime is effective exactly when

`A < 0`, or `A >= 0`, `C < 0`, and `q**(-C) * r**A < 1`.

If `A<0`, use `q`. If `A,C>=0`, no monomial has negative valuation.
Otherwise put `B=-C>0`, `t=q**B*r**A`. For a witness `m=q**i*r**j`,
one has `i>0` and `Bj-Ai>0`. If `t>=1`, then
`m**B=t**i*r**(Bj-Ai)>1`, a contradiction. Thus `t<1` is necessary.

For sufficiency set `K=floor((r-1)*t/(1-t))+1`, `i=B*K`, `j=A*K+1`.
With `delta=(1-t)/t`, the binomial theorem gives
`t**(-K)=(1+delta)**K >= 1+K*delta > r`.
Thus `q**i*r**j=r*t**K<1` and its valuation is `-B<0`.

This supplies a rational termination bound. The implementation uses doubling
and binary search for the least positive `k` in this particular family.
It does not claim a globally smallest exponent pair or polynomial bit complexity.
The strict inequality excludes the boundary `t=1`.

## Every positive pair

- Both generators at least one: `E` is empty.
- Both generators at most one: `E` is their denominator-prime union.
- Generators straddling one: reorder and apply the mixed criterion.
- A generator equal to one is covered by the first two cases.

Primes outside the denominator supports have nonnegative monomial valuations.
This explicitly extends the official definition beyond its mixed regime.

## Sums, units, and specified atoms

Effectiveness is equivalent to a denominator prime appearing in any element
`0<x<1`. In a positive polynomial sum every term is at most `x`, and negative
valuation of the sum forces some term to have negative valuation. A positive
integer coefficient cannot create a negative valuation. Powers of a witness
give arbitrarily negative valuations arbitrarily near zero.

If a prime `ell` has nonnegative valuation on both generators and positive
valuation on each generator below one, every semiring element below one has
positive `ell`-valuation; every nonzero element has nonnegative valuation.
A nontrivial unit would force an inverse with negative valuation. Thus units
are `{1}`. This applies with `ell=2,3,2` respectively to the three named pairs.

In each named pair `v_ell(q)=1`. An element below one of valuation one must
contain a monomial of valuation one; the least such monomial is `q`.
In a factorization of `q`, the valuation-zero factor must be at least one.
If larger than one, its cofactor would have valuation one and be below `q`,
a contradiction. Hence `q` is an atom. The paper expands every step and checks
both monomial regimes. In the third example `2/3` is reducible:
`(2/5)*(1+2/3)=2/3`, with both factors nonunits.

## What is not proved

None of these results resolves atomicity or IDF for any named monoid, or the
general or monogenic open questions. Novelty is unverified.
[Open Problem 2](https://artofproblemsolving.com/polymath/mitprimes2026/p/open-prob2)
reports prior non-ACCP and non-atomic-or-non-IDF progress; this disjunction does
not decide which property fails. The paper attributes known one-generator
results and separately labels announced work without a located complete proof.
Finite checks supplement the proofs; they are not formal verification of
infinite-monoid assertions.

