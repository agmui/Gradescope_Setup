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
        os.system("make simple_test")
        process = subprocess.Popen(['./simple_test'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)

        result = result.lower()
        self.assertTrue(re.search("test( \d)? passed", result), "did not contain \"Test Passed\" in output")
        self.assertTrue(re.search("test crashed", result), "a test did not crash")
        self.assertTrue(re.search("test timed? out", result), "a test did not time out")


if __name__ == '__main__':
    unittest.main()
