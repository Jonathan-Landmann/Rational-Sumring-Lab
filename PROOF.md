# Exact effectiveness criterion

**Scope:** A proven lemma about effective denominator primes, **not** a proof of atomicity, non-atomicity, IDF, or non-IDF of the multiplicative monoid.

Let q,r be positive rationals with 0<q<1<r. A prime p is *effective* if some i,j in N_0 satisfy q^i r^j<1 and v_p(q^i r^j)<0.

## Theorem
Set A=v_p(q) and C=v_p(r). Then p is effective if and only if

1. A<0, or
2. A>=0, C<0, and q^(-C) r^A<1.

## Proof
If A<0, take (i,j)=(1,0). If A>=0 and C>=0, no nonnegative linear combination iA+jC is negative.

Suppose A>=0 and C=-B<0, B>0. We require simultaneously q^i r^j<1 and Ai-Bj<0. Necessarily i>0. Taking logarithms, the inequalities become

A/B < j/i < log(1/q)/log(r).

There exist positive integers i,j with their ratio strictly inside this interval if and only if its left endpoint is strictly smaller than its right endpoint (density of Q in R). This is equivalent to A log(r)<B log(1/q), or q^B r^A<1. QED.

## Examples
- (6/35,19/3): E={5,7}. The candidate p=3 has A=1, C=-1, and qr=114/105>1, hence is not effective.
- (3/10,7/5): E={2,5}. The numerator prime 3 has A=1,C=0, hence is not effective.
- (2/5,2/3): E={3,5}. Both denominator primes occur in generators below 1.

## Research integrity
This is an independently derived elementary characterization; its novelty relative to prior literature and CrowdMath discussions is **unverified**. The conjectures on atomicity and IDF remain open here.
