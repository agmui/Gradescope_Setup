import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt


os.chdir("src")
os.system("make")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_us1tests(self):
        """autograder us1tests.c tests"""
        print(text2art("hybrid threads", "rand"))
        process = subprocess.Popen(['./us1tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("2")
    def test_standalone1(self):
        """autograder standalone1 tests"""
        process = subprocess.Popen(['./standalone1'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertEqual(result.split('\n')[-2], 'done', "last output is not done")


    @weight(0)
    @number("3")
    def test_basic_para(self):
        """autograder basic_para tests"""
        process = subprocess.Popen(['./basic_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result, 'failed basic_para tests')

    @weight(0)
    @number("4a")
    def test_create_para_a(self):
        """autograder create_para try1 tests"""
        process = subprocess.Popen(['./create_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("4b")
    def test_create_para_b(self):
        """autograder create_para try2 tests"""
        process = subprocess.Popen(['./create_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("4c")
    def test_create_para_c(self):
        """autograder create_para try3 tests"""
        process = subprocess.Popen(['./create_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)


if __name__ == '__main__':
    unittest.main()
