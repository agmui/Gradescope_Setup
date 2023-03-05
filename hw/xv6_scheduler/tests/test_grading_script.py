import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt

os.chdir("../src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        print(text2art("stack smashing", "rand"))
        os.system("sudo apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu")
        os.system("tar xf submit-lab-sched.tar")
        process = subprocess.Popen(['make grade'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)


if __name__ == '__main__':
    unittest.main()
