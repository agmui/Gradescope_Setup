import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt

def ascii_art():
    art_1 = art("coffee")  # return art as str in normal mode
    print("a coffee cup for u", art_1)
    # Return ASCII text (default font) and default chr_ignore=True
    Art = text2art("art")
    print(Art)
    # Return ASCII text with block font
    Art = text2art("art", font='block', chr_ignore=True)
    print(Art)
    Art = text2art("test", "rand")  # random font mode
    print(Art)


os.system("../src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        os.system("make clean")
        os.system("make")

    @weight(0)
    @number("1")
    def test_us1tests(self):
        """autograder us1tests.c tests"""
        process = subprocess.Popen(['./us1tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test1=========")
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("2")
    def test_standalone1(self):
        """autograder basic_para tests"""
        process = subprocess.Popen(['./standalone1'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test2=========")
        print(result)
        self.assertEqual(result.split('\n')[-2], 'done', "last output is not done")


    @weight(0)
    @number("3")
    def test_basic_para(self):
        """autograder basic_para tests"""
        process = subprocess.Popen(['./basic_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test3=========")
        print(result)
        self.assertTrue("OK" in result, 'failed basic_para tests')

    @weight(0)
    @number("4a")
    def test_create_para_a(self):
        """autograder create_para tests"""
        process = subprocess.Popen(['./create_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test4a=========")
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("4b")
    def test_create_para_b(self):
        """autograder create_para tests"""
        process = subprocess.Popen(['./create_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test4b=========")
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("4c")
    def test_create_para_c(self):
        """autograder create_para tests"""
        process = subprocess.Popen(['./create_para_tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test4c=========")
        print(result)
        self.assertTrue("OK" in result)


if __name__ == '__main__':
    unittest.main()
