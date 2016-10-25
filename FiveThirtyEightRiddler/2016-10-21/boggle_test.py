from boggle import neighbors
import nose

def test_neigh_1():
    assert set(neighbors(0,0)) == {(0,0),(1,0),(1,1),(0,1)}

def test_neigh_2():
    assert set(neighbors(3,3)) == {(2,2),(2,3),(3,2),(3,3)}

nose.main()
