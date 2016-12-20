from unittest import TestCase
from CodeEval.challenge_41 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual(0, challenge("5;0,1,2,3,0"))

    def test_input_2(self):
        self.assertEqual(4, challenge("20;0,1,10,3,2,4,5,7,6,8,11,9,15,12,13,4,16,18,17,14"))
