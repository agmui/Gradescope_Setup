import os
import sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.gradelib import *  # this is allowed bc of the sys.path.insert
from hw.grading_utils.gradelib import TESTS
from hw.grading_utils.random_utils import capture_output

prev_cwd = os.getcwd()
os.chdir("src/csse332-labs/xv6-riscv")

r = Runner(save("xv6.out"))
#TODO: submission that broke
#https://www.gradescope.com/courses/742262/assignments/4143123/submissions/242113952?view=results#


@test(10, "buddy_allocator, test get buddy")
def test_get_buddy():
    r.run_qemu(shell_script(['buddy_test 0']))
    r.match("^test_get_buddy\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(20, "buddy_allocator, test basic alloc")
def test_basic_alloc():
    r.run_qemu(shell_script(['buddy_test 1']))
    r.match("^test_basic_alloc\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(20, "buddy_allocator, test basic free")
def test_basic_free():
    r.run_qemu(shell_script(['buddy_test 2']))
    r.match("^test_basic_free\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(15, "buddy_allocator, test wrong size coalesce")
def test_wrong_size_coalesce():
    r.run_qemu(shell_script(['buddy_test 3']))
    r.match("^test_wrong_size_coalesce\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "buddy_allocator, test gracefully run out of memory")
def test_gracefully_run_out_of_memory():
    r.run_qemu(shell_script(['buddy_test 4']))
    r.match("^test_gracefully_run_out_of_memory\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "buddy_allocator, test stress big heap chunks")
def test_stress_big_heap_chunks():
    r.run_qemu(shell_script(['buddy_test 5']))
    r.match("^test_stress_big_heap_chunks\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(15, "buddy_allocator, test stress overlapping")
def test_stress_overlapping():
    r.run_qemu(shell_script(['buddy_test 6']))
    r.match("^test_stress_overlapping\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])

output, error = capture_output(run_tests)
output_arr = output.split('\n')
os.chdir(prev_cwd)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        print("================= please go to: =================")
        print("https://docs.google.com/forms/d/e/1FAIpQLSfhQQLJKwMup5vkAd9BBnEZTGOpYZHjvfSJg8V4YlQKp9TufA/viewform")
        print("thank you\n")

    @weight(0)
    @number("1")
    def test_run_grade_lab_buddy(self):
        """output of grade-lab-buddy.py"""
        print(output)
        self.assertIsNone(error, "you did not pass all the tests :c")

    @weight(0)
    @number("2")
    def test_get_buddy(self):
        """autograder get buddy tests"""
        print(output_arr[0])
        self.assertTrue(TESTS[0].ok)

    @weight(0)
    @number("3")
    def test_basic_alloc(self):
        """autograder basic alloc tests"""
        print(output_arr[1])
        self.assertTrue(TESTS[1].ok)

    @weight(0)
    @number("4")
    def test_basic_free(self):
        """autograder basic free tests"""
        print(output_arr[2])
        self.assertTrue(TESTS[2].ok)

    @weight(0)
    @number("5")
    def test_wrong_size_coalesce(self):
        """autograder wrong size coalesce tests"""
        print(output_arr[3])
        self.assertTrue(TESTS[3].ok)

    @weight(0)
    @number("6")
    def test_graceful(self):
        """autograder gracefully run out of memory tests"""
        print(output_arr[4])
        self.assertTrue(TESTS[4].ok)

    @weight(0)
    @number("7")
    def test_stress_big_heap(self):
        """autograder stress big heap chunks tests"""
        print(output_arr[5])
        self.assertTrue(TESTS[5].ok)

    @weight(0)
    @number("8")
    def test_stress_overlap(self):
        """autograder stress overlapping tests"""
        print(output_arr[6])
        self.assertTrue(TESTS[6].ok)


if __name__ == '__main__':
    unittest.main()
