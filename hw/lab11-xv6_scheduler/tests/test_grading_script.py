import os
import subprocess
import sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt
# from gradelib import *
# from gradelib import TESTS
import re

sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.gradelib import *  # this is allowed bc of the sys.path.insert
from hw.grading_utils.gradelib import TESTS
from hw.grading_utils.random_utils import capture_output

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

output, error = capture_output(run_tests)
output_arr = output.split('\n')

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder forkforkfork tests"""
        for i in output_arr:
            print(i)
        #FIXME: print(output_arr[0])
        self.assertTrue(TESTS[0].ok)


if __name__ == '__main__':
    unittest.main()
