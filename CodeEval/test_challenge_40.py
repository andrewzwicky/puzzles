from unittest import TestCase
from CodeEval.challenge_40 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual(1, challenge("2020"))

    def test_input_2(self):
        self.assertEqual(0, challenge("22"))

    def test_input_3(self):
        self.assertEqual(1, challenge("1210"))
