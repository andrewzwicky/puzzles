from unittest import TestCase
from CodeEval.challenge_83 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual(152, challenge("ABbCcc"))

    def test_input_2(self):
        self.assertEqual(754, challenge("Good luck in the Facebook Hacker Cup this year!"))

    def test_input_3(self):
        self.assertEqual(491, challenge("Ignore punctuation, please :)"))

    def test_input_4(self):
        self.assertEqual(729, challenge("Sometimes test cases are hard to make up."))

    def test_input_5(self):
        self.assertEqual(646, challenge("So I just go consult Professor Dalves"))