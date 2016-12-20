from unittest import TestCase
from CodeEval.challenge_124 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual("1245,58,2587,1563,136", challenge("Rkbs,5453; Wdqiz,1245; Rwds,3890; Ujma,5589; Tbzmo,1303;"))

    def test_input_2(self):
        self.assertEqual("70,2489,67,1135,197", challenge("Vgdfz,70; Mgknxpi,3958; Nsptghk,2626; Wuzp,2559; Jcdwi,3761;"))

    def test_input_3(self):
        self.assertEqual("1240,2344,1779,357,279", challenge("Yvnzjwk,5363; Pkabj,5999; Xznvb,3584; Jfksvx,1240; Inwm,5720;"))

    def test_input_4(self):
        self.assertEqual("2683,2553", challenge("Ramytdb,2683; Voclqmb,5236;"))