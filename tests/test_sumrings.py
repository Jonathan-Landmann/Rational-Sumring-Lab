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



def test_state_limit_counts_union_and_checks_on_insertion():
    import pytest
    # Each individual layer has one state; their union has three states.
    with pytest.raises(RuntimeError, match='state limit'):
        enumerate_sumring(F(1), F(1), degree=0, coefficient_sum=2, max_states=2)
    assert enumerate_sumring(F(1), F(1), 0, 2, 3) == {F(0), F(1), F(2)}


def test_zero_coefficient_budget():
    assert enumerate_sumring(F(2, 5), F(2, 3), 100, 0, 1) == {F(0)}


def test_known_units_do_not_count_as_nonunit_factors():
    from sumrings import bounded_factorization_candidates, bounded_irreducibles
    sample = {F(0), F(1), F(2), F(1, 2), F(3), F(6)}
    # 2 and 1/2 are witnessed units; 6=2*3 must not discard 6 as a nonunit split.
    assert bounded_factorization_candidates(sample) == [F(3), F(6)]
    assert bounded_irreducibles(sample) == [F(3), F(6)]


def test_unknown_unit_caveat_remains_sample_based():
    from sumrings import bounded_factorization_candidates
    # 2*3=6 is a sample split. The sample cannot decide if 2 or 3 is a true unit.
    assert bounded_factorization_candidates({F(1), F(2), F(3), F(6)}) == [F(2), F(3)]


def test_integer_primality_and_factorization():
    import pytest
    from sumrings import is_prime, prime_factors
    assert is_prime(104729)
    assert not is_prime(104729**2)
    assert not is_prime(10**400)  # no float overflow in an integer API
    assert prime_factors(-360) == [2, 3, 5]
    assert prime_factors(1) == []
    assert valuation(F(-8, 25), 2) == 3
    for p in [4, 5.0, True]:
        with pytest.raises(ValueError):
            valuation(F(1, 5), p)
    with pytest.raises(ValueError):
        prime_factors(0)
    with pytest.raises(TypeError):
        valuation(0.2, 5)


def test_invalid_budgets_and_nonpositive_generators():
    import pytest
    for degree in [-1, 1.0, True]:
        with pytest.raises(ValueError):
            generators(F(1, 2), F(2), degree)
    for bound in [-1, 1.0, True]:
        with pytest.raises(ValueError):
            effective_prime_witnesses(F(1, 2), F(2), bound)
    with pytest.raises(ValueError):
        enumerate_sumring(F(1), F(1), max_states=0)
    for q, r in [(F(0), F(2)), (F(1), F(-1))]:
        with pytest.raises(ValueError):
            generators(q, r, 1)
    with pytest.raises(TypeError):
        generators(0.5, 2, 1)


def test_divisors_require_positive_target():
    import pytest
    with pytest.raises(ValueError):
        bounded_divisors({F(0), F(1)}, F(0))
    with pytest.raises(TypeError):
        bounded_divisors({F(1)}, 1.0)
