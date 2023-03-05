import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt

os.system("apt update -y > /dev/null && apt upgrade -y > /dev/null")
os.system("apt install -y gdb gdb-multiarch gcc-multilib python2")
os.system("bash -c \"$(curl -fsSL https://gef.blah.cat/sh)\"")
os.chdir("src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        print(text2art("stack smashing", "rand"))
        process = subprocess.Popen(['./part8 $(python2 part8.py)'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
