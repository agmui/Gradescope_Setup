import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt


os.chdir("src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

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
        self.assertTrue("Test Timed Out" in result and "Test Passed" in result)


if __name__ == '__main__':
    unittest.main()
