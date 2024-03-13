import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt
from gradelib import *
from gradelib import TESTS
import re

os.chdir("src/csse332-labs/xv6-riscv")

r = Runner(save("xv6.out"))

@test(0, "running forkforkfork")
def test_forkforkfork():
    r.run_qemu(shell_script([
        'usertests forkforkfork'
    ]))

@test(100, "forkforkfork", parent=test_forkforkfork)
def test_simple():
    matches = re.findall("^test forkforkfork: OK$", r.qemu.output, re.M)
    assert_equal(len(matches), 1, "Number of appearances of 'forkforkfork: OK'")

run_tests()
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        # os.system("sudo apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu")
        # os.system("tar xf submit-lab-sched.tar")
        # process = subprocess.Popen(['make grade'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        # print(result)
        # self.assertTrue("OK" in result)
        self.assertTrue(TESTS[0].ok)


if __name__ == '__main__':
    unittest.main()
