from unittest import TestCase
from CodeEval.challenge_19 import challenge


class Challenge19Test(TestCase):
    def test_input_1(self):
        self.assertEqual("true", challenge("86,2,3"))

    def test_input_2(self):
        self.assertEqual("false", challenge("125,1,2"))
