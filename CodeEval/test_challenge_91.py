from unittest import TestCase
from CodeEval.challenge_91 import challenge


class ChallengeTest(TestCase):
    def test_input_1(self):
        self.assertEqual("-38.797 7.581 14.354 70.920 90.374 99.323",
                         challenge("70.920 -38.797 14.354 99.323 90.374 7.581"))

    def test_input_2(self):
        self.assertEqual("-55.552 -37.507 -3.263 27.999 40.079 65.213",
                         challenge("-37.507 -3.263 40.079 27.999 65.213 -55.552"))
