import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
from gradelib import *
from gradelib import TESTS

os.chdir("/autograder/source/src/xv6-riscv")

r = Runner(save("xv6.out"))

@test(5, "rhmm, test basic case")
def test_basic_case():
    r.run_qemu(shell_script(['lab01basic']))
    r.match("^TestCase1:.*: Ok\.",
            no=[".*FAILED.*"])

@test(20, "rhmm, test basic alloc")
def test_basic_alloc():
    r.run_qemu(shell_script(['lab01test 1']))
    r.match("^test_basic_alloc\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(20, "rhmm, test basic free")
def test_basic_free():
    r.run_qemu(shell_script(['lab01test 2']))
    r.match("^test_basic_free\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "rhmm, test coalesce basic 1")
def test_coalesce_basic1():
    r.run_qemu(shell_script(['lab01test 3']))
    r.match("^test_coalesce_basic1\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "rhmm, test coalesce basic 2")
def test_coalesce_basic2():
    r.run_qemu(shell_script(['lab01test 4']))
    r.match("^test_coalesce_basic2\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "rhmm, test coalesce 3")
def test_coalesce3():
    r.run_qemu(shell_script(['lab01test 5']))
    r.match("^test_coalesce3\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "rhmm, test force alignment")
def test_foce_alignment():
    r.run_qemu(shell_script(['lab01test 6']))
    r.match("^test_force_alignment\\(\\d+\\): OK\.",
            no=[".*Assertiona FAILED.*"])


@test(10, "rhmm, test too small blocks")
def test_too_small_blocks():
    r.run_qemu(shell_script(['lab01test 7']))
    r.match("^test_too_small_blocks\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "rhmm, test gracefully run out of memory")
def test_gracefully_run_out_of_memory():
    r.run_qemu(shell_script(['lab01test 8']))
    r.match("^test_gracefully_run_out_of_memory\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(15, "rhmm, test stress big heap chunks")
def test_stress_big_heap_chunks():
    r.run_qemu(shell_script(['lab01test 9']))
    r.match("^test_stress_big_heap_chunks\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(20, "rhmm, test stress overlapping")
def test_stress_overlapping():
    r.run_qemu(shell_script(['lab01test 10']))
    r.match(no=[".*Assertion FAILED.*"])


run_tests()


class TestIntegration(unittest.TestCase):
    def setUp(self):
        print("================= please go to: =================")
        print("https://docs.google.com/forms/d/e/1FAIpQLSfhQQLJKwMup5vkAd9BBnEZTGOpYZHjvfSJg8V4YlQKp9TufA/viewform")
        print("thank you")

    @weight(0)
    @number("1")
    def test_basic_case(self):
        """autograder basic case tests"""
        print(text2art("heap manager", "rand"))
        self.assertTrue(TESTS[0].ok)

    @weight(0)
    @number("2")
    def test_basic_alloc(self):
        """autograder basic alloc tests"""
        self.assertTrue(TESTS[1].ok)

    @weight(0)
    @number("3")
    def test_basic_free(self):
        """autograder basic free tests"""
        self.assertTrue(TESTS[2].ok)

    @weight(0)
    @number("4")
    def test_coalesce_basic1(self):
        """autograder coalesce basic1 tests"""
        self.assertTrue(TESTS[3].ok)

    @weight(0)
    @number("5")
    def test_coalesce_basic2(self):
        """autograder coalesce basic2 tests"""
        self.assertTrue(TESTS[4].ok)

    @weight(0)
    @number("6")
    def test_coalesce3(self):
        """autograder coalesce basic3 tests"""
        self.assertTrue(TESTS[5].ok)

    @weight(0)
    @number("7")
    def test_foce_alignment(self):
        """autograder foce alignment tests"""
        self.assertTrue(TESTS[6].ok)

    @weight(0)
    @number("8")
    def test_too_small_blocks(self):
        """autograder too small blocks tests"""
        self.assertTrue(TESTS[7].ok)

    @weight(0)
    @number("9")
    def test_gracefully_run_out_of_memory(self):
        """autograder gracefully run out of mem tests"""
        self.assertTrue(TESTS[8].ok)

    @weight(0)
    @number("10")
    def test_stress_big_heap_chunks(self):
        """autograder biiiggg yoshi tests"""
        self.assertTrue(TESTS[9].ok)

    @weight(0)
    @number("11")
    def test_stress_overlapping(self):
        """autograder stress overlapping tests"""
        self.assertTrue(TESTS[10].ok)

if __name__ == '__main__':
    unittest.main()
