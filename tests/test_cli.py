import pytest
from cli import main


def test_cli_reports_exact_primes_for_both_below_one(capsys):
    main(['--q', '2/5', '--r', '2/3', '--degree', '1', '--coefficients', '1'])
    output = capsys.readouterr().out
    assert 'Effective denominator primes (exact): [3, 5]' in output
    assert 'p=3: i=0, j=1' in output
    assert 'NOT certified atoms' in output


def test_cli_optional_bounded_search_is_separate(capsys):
    main(['--q', '2/5', '--r', '2/3', '--exponents', '0', '--degree', '0'])
    output = capsys.readouterr().out
    assert 'Effective denominator primes (exact): [3, 5]' in output
    assert 'optional exponent bound: []' in output


@pytest.mark.parametrize('option,value', [
    ('--q', '0'), ('--q', '1/0'), ('--r', '-1'), ('--degree', '-1'),
    ('--coefficients', '-1'), ('--exponents', '-1'), ('--max-states', '0'),
    ('--target', '0'),
])
def test_cli_invalid_input_is_usage_error(option, value, capsys):
    args = ['--q', '2/5', '--r', '2/3', option, value]
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 2
    assert 'error:' in capsys.readouterr().err


def test_cli_state_limit_is_clear_error(capsys):
    with pytest.raises(SystemExit) as error:
        main(['--q', '1', '--r', '1', '--max-states', '1'])
    assert error.value.code == 2
    assert 'state limit exceeded' in capsys.readouterr().err
