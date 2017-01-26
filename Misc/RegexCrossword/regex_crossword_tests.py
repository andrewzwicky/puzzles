import pytest
from regex_crossword import HexGrid

LETTERS = """NHPEHAS\
DIOMOMTH\
FOXNXAXPH\
MMOMMMMRHH\
MCXNMMCRXEM\
CMCCCCMMMMMM\
HRXRCMIIIHXLS\
OREOREOREORE\
VCXCCHHMXCC\
RRRRHHHRRU\
NCXDXEXLE\
RRDDMMMM\
GCCHHCC"""


@pytest.mark.parametrize("index,expected", [
    (-6, "NHPEHAS"),
    (-5, "DIOMOMTH"),
    (-4, "FOXNXAXPH"),
    (-3, "MMOMMMMRHH"),
    (-2, "MCXNMMCRXEM"),
    (-1, "CMCCCCMMMMMM"),
    (0, "HRXRCMIIIHXLS"),
    (1, "OREOREOREORE"),
    (2, "VCXCCHHMXCC"),
    (3, "RRRRHHHRRU"),
    (4, "NCXDXEXLE"),
    (5, "RRDDMMMM"),
    (6, "GCCHHCC")
])
def test_z_rows(index, expected):

    g = HexGrid(LETTERS)
    assert g.get_z_row(index) == expected


@pytest.mark.parametrize("index,expected", [
    (6, 'NDFMMCH'),
    (5, 'HIOMCMRO'),
    (4, 'POXOXCXRV'),
    (3, 'EMNMNCRECR'),
    (2, 'HOXMMCCOXRN'),
    (1, 'AMAMMCMRCRCR'),
    (0, 'STXMCMIECRXRG'),
    (-1, 'HPRRMIOHHDDC'),
    (-2, 'HHXMIRHHXDC'),
    (-3, 'HEMHEMHEMH'),
    (-4, 'MMXOXRXMH'),
    (-5, 'MLRCRLMC'),
    (-6, 'SECUEMC')
])
def test_y_rows(index, expected):
    g = HexGrid(LETTERS)
    assert g.get_y_row(index) == expected


@pytest.mark.parametrize("index,expected", [
    (-6, 'GRNRVOH'),
    (-5, 'CRCRCRRC'),
    (-4, 'CDXRXEXMM'),
    (-3, 'HDDRCORCCM'),
    (-2, 'HMXHCRCCXMF'),
    (-1, 'CMEHHEMCNOOD'),
    (0, 'CMXHHOICMMXIN'),
    (1, 'MLRMRIMMMNOH'),
    (2, 'ERXEIMCMXMP'),
    (3, 'UCOHMRMAOE'),
    (4, 'CRXMXRXMH'),
    (5, 'ELMEHPTA'),
    (6, 'SMMHHHS')
])
def test_x_rows(index, expected):
    g = HexGrid(LETTERS)
    assert g.get_x_row(index) == expected


def test_same_output():
    g = HexGrid(LETTERS)
    assert g.get_string() == LETTERS