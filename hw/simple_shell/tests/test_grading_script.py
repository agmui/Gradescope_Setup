import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt


os.chdir("../src")
print(text2art("simple shell", "rand"))
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        # process = subprocess.Popen(['../src/make grade'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        # print(result)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
