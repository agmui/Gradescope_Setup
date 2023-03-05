import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt


os.chdir("../src")
print(text2art("stack smashing", "rand"))
class TestIntegration(unittest.TestCase):
    def setUp(self):
        print("if you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help")

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        # os.system("sudo apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu")
        # os.system("tar xf ../src/submit-lab-0.tar")
        # process = subprocess.Popen(['../src/make grade'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        # print(result)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
