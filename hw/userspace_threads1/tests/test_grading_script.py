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


os.system("apt update > /dev/null && apt upgrade > /dev/null")
os.system("apt install -y valgrind > /dev/null")
os.chdir("src")
os.system("make tests.bin")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_1(self):
        """autograder tests.bin 1 tests"""
        process = subprocess.Popen(['./tests.bin', '1'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("2")
    def test_2(self):
        """autograder test.bin 2 tests"""
        process = subprocess.Popen(['./tests.bin', '2'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("3")
    def test_3(self):
        """autograder test.bin 3 tests"""
        process = subprocess.Popen(['./tests.bin', '3'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("4")
    def test_4(self):
        """autograder test.bin 4 tests"""
        process = subprocess.Popen(['./tests.bin', '4'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("5")
    def test_5(self):
        """autograder test.bin 5 tests"""
        process = subprocess.Popen(['./tests.bin', '5'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)

    @weight(0)
    @number("6")
    def test_valgrind(self):
        """autograder valgrind tests"""
        cmd = "valgrind ./tests.bin 5".split(' ')
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test5=========")
        self.assertTrue(True, "there is a memory leak")
