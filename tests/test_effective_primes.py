from fractions import Fraction as F
from effective_primes import effective_primes_exact
from sumrings import effective_prime_witnesses

def test_named_pairs():
    assert effective_primes_exact(F(6,35),F(19,3)) == {5,7}
    assert effective_primes_exact(F(3,10),F(7,5)) == {2,5}
    assert effective_primes_exact(F(2,5),F(2,3)) == {3,5}

def test_finite_witnesses_are_sound():
    for a,b,c,d in [(6,35,19,3),(3,10,7,5),(2,5,2,3),(3,8,5,2)]:
        q,r=F(a,b),F(c,d)
        assert set(effective_prime_witnesses(q,r,12)).issubset(effective_primes_exact(q,r))

def test_boundary_case():
    # q*r=1: strict inequality must fail for p=3
    assert effective_primes_exact(F(2,3),F(3,2)) == {3}
