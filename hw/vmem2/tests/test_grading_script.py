import os
import unittest
import re
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
from gradelib import *
from gradelib import TESTS

os.chdir("src")
os.system("apt update -y > /dev/null && apt upgrade -y > /dev/null")
os.system("apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu > /dev/null")
os.system("tar xf submit-lab-5.tar")
os.system("make > /dev/null")

r = Runner(save("xv6.out"))

@test(0, "running cowtest")
def test_cowtest():
    r.run_qemu(shell_script([
        'cowtest'
    ]))

@test(40, "simple", parent=test_cowtest)
def test_simple():
    matches = re.findall("^simple: ok$", r.qemu.output, re.M)
    assert_equal(len(matches), 2, "Number of appearances of 'simple: ok'")

@test(40, "three", parent=test_cowtest)
def test_three():
    matches = re.findall("^three: ok$", r.qemu.output, re.M)
    assert_equal(len(matches), 3, "Number of appearances of 'three: ok'")

@test(20, "file", parent=test_cowtest)
def test_file():
    r.match('^file: ok$')


run_tests()

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    def test_cowtest(self):
        """cowtest"""
        print(text2art("stack smashing", "rand"))
        self.assertTrue(TESTS[0].ok)

    def test_simple(self):
        """simple"""
        self.assertTrue(TESTS[1].ok)

    def test_three(self):
        """three"""
        self.assertTrue(TESTS[2].ok)

    def test_file(self):
        """file"""
        self.assertTrue(TESTS[3].ok)



if __name__ == '__main__':
    unittest.main()
