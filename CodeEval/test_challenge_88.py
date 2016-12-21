from unittest import TestCase
from CodeEval.challenge_88 import challenge, Circuit, Juggler


test_case = """
C C0 H:7 E:7 P:10
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

C0 = Circuit(0, 7, 7, 10)
C1 = Circuit(1, 2, 1, 1)
C2 = Circuit(2, 7, 6, 4)

J0 = Juggler(0, 3, 9, 2, [C2, C0, C1])
J1 = Juggler(1, 4, 3, 7, [C0, C2, C1])
J2 = Juggler(2, 4, 0, 10, [C0, C2, C1])
J3 = Juggler(3, 10, 3, 8, [C2, C0, C1])
J4 = Juggler(4, 6, 10, 1, [C0, C2, C1])
J5 = Juggler(5, 6, 7, 7, [C0, C2, C1])
J6 = Juggler(6, 8, 6, 9, [C2, C1, C0])
J7 = Juggler(7, 7, 1, 5, [C2, C1, C0])
J8 = Juggler(8, 8, 2, 3, [C1, C0, C2])
J9 = Juggler(9, 10, 2, 1, [C1, C2, C0])
J10 = Juggler(10, 6, 4, 5, [C0, C2, C1])
J11 = Juggler(11, 8, 4, 7, [C0, C1, C2])

C0.assigned_jugglers = [J6, J3, J10, J0]
C1.assigned_jugglers = [J9, J8, J7, J1]
C2.assigned_jugglers = [J5, J11, J2, J4]

output = [C0, C1, C2]


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertListEqual(output, challenge(test_case))