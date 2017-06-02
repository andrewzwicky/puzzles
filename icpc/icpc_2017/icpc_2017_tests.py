import os
import pytest
import math
from icpc_2017.e_speed import e_speed
from icpc_2017.b_clue import b_clue
from icpc_2017.c_improbable import c_improbable

TEST_DATA_FOLDER = "icpc/icpc_2017/test_data/"

def get_test_data(folder):
    folder = os.path.join(TEST_DATA_FOLDER, folder)
    ins = []
    ans = []

    for file in sorted(os.listdir(folder)):
        full_file_path = os.path.join(folder, file)
        if file.endswith(".in"):
            with open(full_file_path, 'r') as in_file:
                ins.append(in_file.read().lstrip().rstrip())

        if file.endswith(".ans"):
            with open(full_file_path, 'r') as ans_file:
                ans.append(ans_file.read().lstrip().rstrip())

    return [(i, a) for i, a in zip(ins, ans)]


def get_test_ids(folder):
    folder = os.path.join(TEST_DATA_FOLDER, folder)
    names = []
    for file in sorted(os.listdir(folder)):
        if file.endswith(".in"):
            names.append(os.path.basename(file))

    return names

@pytest.mark.parametrize("input_string,expected",
                         get_test_data("B-clue"),
                         ids=get_test_ids("B-clue"))
#@pytest.mark.timeout(1)
def test_b_clue(input_string, expected):
    assert b_clue(input_string) == expected


@pytest.mark.parametrize("input_string,expected",
                         get_test_data("E-speed"),
                         ids=get_test_ids("E-speed"))
@pytest.mark.timeout(1)
@pytest.mark.skip()
def test_e_speed(input_string, expected):
    assert math.isclose(e_speed(input_string),float(expected), rel_tol=10**-6, abs_tol=10**-6)


@pytest.mark.parametrize("input_string,expected",
                         get_test_data("C-improbable"),
                         ids=get_test_ids("C-improbable"))
@pytest.mark.timeout(1)
@pytest.mark.skip()
def test_c_improbable(input_string, expected):
    assert c_improbable(input_string) == int(expected)
