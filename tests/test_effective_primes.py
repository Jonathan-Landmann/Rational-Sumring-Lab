from fractions import Fraction as F
import pytest
from effective_primes import effective_primes_exact
from sumrings import effective_prime_witnesses


@pytest.mark.parametrize('q,r,expected', [
    (F(6, 35), F(19, 3), {5, 7}),
    (F(3, 10), F(7, 5), {2, 5}),
    (F(2, 5), F(2, 3), {3, 5}),
    (F(2, 3), F(3, 2), {3}),
    (F(2, 5), F(3, 2), {2, 5}),
    (F(2, 3), F(5, 2), {3}),
    (F(1), F(2, 3), {3}),
    (F(1), F(3, 2), set()),
    (F(1), F(1), set()),
    (F(3, 2), F(7, 5), set()),
])
def test_named_pairs_and_all_regimes(q, r, expected):
    assert effective_primes_exact(q, r) == expected
    assert effective_primes_exact(r, q) == expected


def test_finite_witnesses_are_sound():
    for a, b, c, d in [(6, 35, 19, 3), (3, 10, 7, 5), (2, 5, 2, 3), (3, 8, 5, 2)]:
        q, r = F(a, b), F(c, d)
        assert set(effective_prime_witnesses(q, r, 12)).issubset(effective_primes_exact(q, r))


def test_boundary_case():
    # q*r=1: strict inequality fails for p=2 (p=3 is witnessed by q).
    assert effective_primes_exact(F(2, 3), F(3, 2)) == {3}


def test_independent_small_grid_witnesses():
    # The oracle inspects reduced denominators, not the valuation/decision code.
    rationals = sorted({F(a, b) for a in range(1, 6) for b in range(1, 6)})
    for q in rationals:
        for r in rationals:
            found = set()
            for i in range(7):
                for j in range(7):
                    x = q**i * r**j
                    if x < 1:
                        found.update(p for p in (2, 3, 5) if x.denominator % p == 0)
            assert found <= effective_primes_exact(q, r)
            assert effective_primes_exact(q, r) == effective_primes_exact(r, q)


@pytest.mark.parametrize('q,r', [(F(0), F(2)), (F(-1), F(2)), (F(1), F(0))])
def test_nonpositive_inputs_rejected(q, r):
    with pytest.raises(ValueError):
        effective_primes_exact(q, r)
    with pytest.raises(ValueError):
        effective_prime_witnesses(q, r)


@pytest.mark.parametrize('bad', [0.5, '1/2', True])
def test_inexact_inputs_rejected(bad):
    with pytest.raises(TypeError):
        effective_primes_exact(bad, F(2))


def test_zero_exponent_bound_is_not_ineffectiveness():
    assert effective_prime_witnesses(F(2, 5), F(2, 3), 0) == {}
    assert effective_primes_exact(F(2, 5), F(2, 3)) == {3, 5}
