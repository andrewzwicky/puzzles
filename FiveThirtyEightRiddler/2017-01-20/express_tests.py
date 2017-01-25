import pytest
from express import binomial


@pytest.mark.parametrize("odds,successes,trials,expected", [
    (0.3, 0, 6, 0.1176),
    (0.3, 1, 6, 0.3025),
    (0.3, 2, 6, 0.3241),
    (0.3, 3, 6, 0.1852),
    (0.3, 4, 6, 0.0595),
    (0.3, 5, 6, 0.0102),
    (0.3, 6, 6, 0.0007),
])
def test_binomial(odds, successes, trials, expected):
    assert abs(binomial(odds, successes, trials) - expected) < .0001
