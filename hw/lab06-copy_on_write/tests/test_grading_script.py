import os
import sys
import re
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.gradelib import *  # this is allowed bc of the sys.path.insert
from hw.grading_utils.gradelib import TESTS
from hw.grading_utils.random_utils import capture_output

prev_cwd = os.getcwd()
os.chdir("src/csse332-labs/xv6-riscv")

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


output, error = capture_output(run_tests)
output_arr = output.split('\n')
os.chdir(prev_cwd)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        print("================= please go to: =================")
        print("https://docs.google.com/forms/d/e/1FAIpQLSfhQQLJKwMup5vkAd9BBnEZTGOpYZHjvfSJg8V4YlQKp9TufA/viewform")

    @number("1")
    def test_aaaa(self):
        """output of grade-lab-<TODO: add file name>.py"""
        print(output)
        self.assertIsNone(error, "you did not pass all the tests :c")

    @number("2")
    def test_cowtest(self):
        """cowtest"""
        os.system("cowsay this do be my lab")
        self.assertTrue(TESTS[0].ok)

    @number("3")
    def test_simple(self):
        """simple test"""
        self.assertTrue(TESTS[1].ok)

    @number("4")
    def test_three(self):
        """three test"""
        self.assertTrue(TESTS[2].ok)

    @number("5")
    def test_file(self):
        """file test"""
        self.assertTrue(TESTS[3].ok)



if __name__ == '__main__':
    unittest.main()
