import pytest
from regex_crossword import HexGrid


@pytest.mark.parametrize("index,expected", [
    (0, ["06-6","05-5","04-4","03-3","02-2","01-1","000","0-11","0-22","0-33","0-44","0-55","0-66"]),
    (1, ["15-6","14-5","13-4","12-3","11-2","10-1","1-10","1-21","1-32","1-43","1-54","1-65"])
])
def test_outside_board(index, expected):
    g = HexGrid(13,None,None,None)
    assert g.get_x_row(index) == expected
