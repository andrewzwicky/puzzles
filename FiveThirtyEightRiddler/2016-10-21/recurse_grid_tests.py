import pytest
import pyximport
pyximport.install()
from recurse_grid import neighbors


@pytest.mark.parametrize("input_square,expected", [
    ((0, 0), [(0, 0), (0, 1), (1, 0), (1, 1)]),
    ((1, 1), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
    ((3, 3), [(2, 2), (2, 3), (3, 2), (3, 3)]),
])
def test_neighbors(input_square, expected):
    assert list(neighbors(*input_square)) == expected


@pytest.mark.parametrize("input_square", [
    (4, 2), (-1, 1), (2, 6), (3, -2)
])
def test_neighbors_outside_board(input_square):
    with pytest.raises(ValueError):
        list(neighbors(*input_square))
