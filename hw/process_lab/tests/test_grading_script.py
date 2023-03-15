import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import re


os.chdir("src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        print("If you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help")

    @weight(0)
    @number("1")
    def test_simple(self):
        """autograder simple_tests"""
        print(text2art("process lab", "rand"))
        os.system("make simple_test")
        print("if the autograder does not work email muian@rose-hulman.edu and tell them they are an idiot and tell them to fix it\n")
        process = subprocess.Popen(['./simple_test'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("Test Passed" in result, "one of the tests did not pass")
        self.assertTrue("Test Timed Out" in result, "tests did not time out")


if __name__ == '__main__':
    unittest.main()
