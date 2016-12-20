from unittest import TestCase
from CodeEval.challenge_8 import challenge


class Challenge7Test(TestCase):
    def test_input_1(self):
        self.assertEqual("World Hello", challenge("Hello World"))

    def test_input_2(self):
        self.assertEqual("CodeEval Hello", challenge("Hello CodeEval"))