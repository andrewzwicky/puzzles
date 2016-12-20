from unittest import TestCase
from CodeEval.challenge_30 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual("4", challenge("1,2,3,4;4,5,6"))

    def test_input_2(self):
        self.assertEqual("", challenge("20,21,22;45,46,47"))

    def test_input_3(self):
        self.assertEqual("8,9", challenge("7,8,9;8,9,10,11,12"))