import os
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
from gradelib import *

os.chdir("src")
os.system("sudo apt install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu")

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

tests = run_tests()


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    def test_add_with_pointers(self):
        """autograder tests"""+tests[0].title
        self.assertTrue(tests[0].ok)
    def test_ensure_correct_order(self):
        """autograder tests"""+tests[1].title
        self.assertTrue(tests[1].ok)
    def test_special_equals(self):
        """autograder tests"""+tests[2].title
        self.assertTrue(tests[2].ok)
    def test_string_with_q(self):
        """autograder tests"""+tests[3].title
        self.assertTrue(tests[3].ok)
    def test_no_arguments(self):
        """autograder tests"""+tests[4].title
        self.assertTrue(tests[4].ok)
    def test_returns(self):
        """autograder tests"""+tests[5].title
        self.assertTrue(tests[5].ok)
    def test_makes_syscall(self):
        """autograder tests"""+tests[6].title
        self.assertTrue(tests[6].ok)
    def test_all(self):
        """autograder tests"""+tests[7].title
        self.assertTrue(tests[7].ok)
    def test_in_current_directory(self):
        """autograder tests"""+tests[8].title
        self.assertTrue(tests[8].ok)
    def test_recursive(self):
        """autograder tests"""+tests[9].title
        self.assertTrue(tests[9].ok)


if __name__ == '__main__':
    unittest.main()
