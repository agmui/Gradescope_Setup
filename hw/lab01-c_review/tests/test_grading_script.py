import os
import sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit

sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.gradelib import *  # this is allowed bc of the sys.path.insert
from hw.grading_utils.gradelib import TESTS
from hw.grading_utils.random_utils import capture_output

#TODO: dont use chdir, try to force all files to
# https://stackoverflow.com/questions/41742317/how-can-i-change-directory-with-python-pathlib
prev_cwd = os.getcwd()
os.chdir("src/csse332-labs/xv6-riscv") # this assumes you are running the file one directory level up

r = Runner(save("xv6.out"))


@test(5, "warmup, add with pointers")
def test_add_with_pointers():
    r.run_qemu(shell_script(['warmup 1']))
    r.match("^test_add_with_pointers\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(5, "warmup, ensure correct order")
def test_ensure_correct_order():
    r.run_qemu(shell_script(['warmup 2']))
    # In here, given the way the regex matching is happening (line by line), we
    # must provide a regex for each line that we'd like to match. If a regex 
    # matches more than one line, then it won't work because they will remove it
    # from the list. 
    r.match("^test_ensure_correct_order\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "warmup, special equals")
def test_special_equals():
    r.run_qemu(shell_script(['warmup 3']))
    r.match("^test_special_equals\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(10, "warmup, string with q")
def test_string_with_q():
    r.run_qemu(shell_script(['warmup 4']))
    r.match("^test_string_with_q\\(\\d+\\): OK\.",
            no=[".*Assertion FAILED.*"])


@test(2, "sleep, no arguments")
def test_sleep_no_args():
    r.run_qemu(shell_script(['sleep']))
    r.match(no=["exec .* failed", "$ sleep\n$"])


@test(3, "sleep, returns")
def test_sleep_returns():
    r.run_qemu(shell_script(['sleep', 'echo OK']))
    r.match("^OK$", no=["exec .* failed", "$ sleep\n$"])


@test(15, "sleep, makes syscall")
def test_sleep():
    r.run_qemu(shell_script(['sleep 10', 'echo FAIL']),
               stop_breakpoint('sys_sleep'))
    r.match("\\$ sleep 10", no=['FAIL'])


@test(20, "arraylist, all")
def test_arraylist():
    r.run_qemu(shell_script(['arraylist']))
    r.match(".*OK.", no=[".*Assertion FAILED.*"])


@test(20, "find, in current directory")
def test_find_curdir():
    fn = random_str()
    r.run_qemu(shell_script([
        'echo > %s' % fn,
        'find . %s' % fn
    ]))
    r.match('\./%s' % fn)


@test(10, "find, recursive")
def test_find_recursive():
    needle = random_str()
    dirs = [random_str() for _ in range(3)]
    r.run_qemu(shell_script([
        'mkdir %s' % dirs[0],
        'echo > %s/%s' % (dirs[0], needle),
        'mkdir %s/%s' % (dirs[0], dirs[1]),
        'echo > %s/%s/%s' % (dirs[0], dirs[1], needle),
        'mkdir %s' % dirs[2],
        'echo > %s/%s' % (dirs[2], needle),
        'find . %s' % needle
    ]))
    r.match('./%s/%s' % (dirs[0], needle),
            './%s/%s/%s' % (dirs[0], dirs[1], needle),
            './%s/%s' % (dirs[2], needle))


output, error = capture_output(run_tests)
output_arr = output.split('\n')
os.chdir(prev_cwd)

class TestIntegration(unittest.TestCase):
    # def setUp(self):
    #     print("if you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help")

    #TODO: use @number instead of aaaaaa
    def test_aaaaaah_run_grading_script(self):
        """output of grade-lib-0.py"""
        print(output) #TODO: add color there is a --color flag in gradelib.py
        self.assertIsNone(error, "you did not pass all the tests :c")

    #TODO: add numbers and points
    def test_add_with_pointers(self):
        """unittest: add with pointers"""
        print(output_arr[0])
        self.assertTrue(TESTS[0].ok, "If you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0")

    def test_ensure_correct_order(self):
        """unittest: ensure_correct_order"""
        print(output_arr[1])
        self.assertTrue(TESTS[1].ok)

    def test_special_equals(self):
        """unittest: special equals"""
        print(output_arr[2])
        self.assertTrue(TESTS[2].ok)

    def test_string_with_q(self):
        """autograde string with q"""
        print(output_arr[3])
        self.assertTrue(TESTS[3].ok)

    def test_no_arguments(self):
        """unittest: no arguments"""
        print(output_arr[4])
        self.assertTrue(TESTS[4].ok)

    def test_returns(self):
        """unittest: returns"""
        print(output_arr[5])
        self.assertTrue(TESTS[5].ok)

    def test_makes_syscall(self):
        """unittest: makes syscall"""
        print(output_arr[6])
        self.assertTrue(TESTS[6].ok)

    def test_all(self):
        """unittest: all"""
        print(output_arr[7])
        self.assertTrue(TESTS[7].ok)

    def test_in_current_directory(self):
        """unittest: in current dir"""
        print(output_arr[8])
        self.assertTrue(TESTS[8].ok)

    def test_recursive(self):
        """unittest: recursive"""
        print(output_arr[9])
        self.assertTrue(TESTS[9].ok)


if __name__ == '__main__':
    unittest.main()
