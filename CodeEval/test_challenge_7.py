from unittest import TestCase
from CodeEval.challenge_7 import challenge


class Challenge7Test(TestCase):
    def test_input_1(self):
        self.assertEqual(5, challenge("- * / 15 - 7 + 1 1 3 + 2 + 1 1"))

    def test_input_2(self):
        self.assertEqual(20, challenge("* + 2 3 4"))