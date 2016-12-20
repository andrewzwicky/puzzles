from unittest import TestCase
from CodeEval.challenge_21 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual(5, challenge("23"))

    def test_input_2(self):
        self.assertEqual(19, challenge("496"))