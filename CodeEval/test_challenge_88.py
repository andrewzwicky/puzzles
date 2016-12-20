from unittest import TestCase
from CodeEval.challenge_88 import challenge


test_case = """C C0 H:7 E:7 P:10
C C1 H:2 E:1 P:1
C C2 H:7 E:6 P:4

J J0 H:3 E:9 P:2 C2,C0,C1
J J1 H:4 E:3 P:7 C0,C2,C1
J J2 H:4 E:0 P:10 C0,C2,C1
J J3 H:10 E:3 P:8 C2,C0,C1
J J4 H:6 E:10 P:1 C0,C2,C1
J J5 H:6 E:7 P:7 C0,C2,C1
J J6 H:8 E:6 P:9 C2,C1,C0
J J7 H:7 E:1 P:5 C2,C1,C0
J J8 H:8 E:2 P:3 C1,C0,C2
J J9 H:10 E:2 P:1 C1,C2,C0
J J10 H:6 E:4 P:5 C0,C2,C1
J J11 H:8 E:4 P:7 C0,C1,C2"""

output = ["C2 J6 C2:128 C1:31 C0:188, J3 C2:120 C0:171 C1:31, J10 C0:120 C2:86 C1:21, J0 C2:83 C0:104 C1:17",
          "C1 J9 C1:23 C2:86 C0:94, J8 C1:21 C0:100 C2:80, J7 C2:75 C1:20 C0:106, J1 C0:119 C2:74 C1:18",
          "C0 J5 C0:161 C2:112 C1:26, J11 C0:154 C1:27 C2:108, J2 C0:128 C2:68 C1:18, J4 C0:122 C2:106 C1:23"]


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual(output, challenge(test_case))
