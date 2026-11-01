from fractions import Fraction as F
from sumrings import (generators, enumerate_sumring, valuation,
                      effective_prime_witnesses, bounded_divisors)

def test_generators():
    assert set(generators(F(2, 5), F(2, 3), 1)) == {F(1), F(2, 5), F(2, 3)}

def test_enumeration():
    x = enumerate_sumring(F(2, 5), F(2, 3), 1, 2)
    assert F(4, 5) in x and F(16, 15) in x and F(0) in x

def test_valuation():
    assert valuation(F(6, 35), 5) == -1
    assert valuation(F(6, 35), 2) == 1

def test_effective_witnesses():
    w = effective_prime_witnesses(F(6, 35), F(19, 3), 4)
    assert 5 in w and 7 in w
    for p, (i, j, x) in w.items():
        assert x < 1 and valuation(x, p) < 0

def test_divisor_witness():
    e = enumerate_sumring(F(2, 5), F(2, 3), 1, 2)
    assert (F(1), F(2)) in bounded_divisors(e, F(2))
