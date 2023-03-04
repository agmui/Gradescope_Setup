import os
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
from gradelib import *
import asyncio # TODO: add to reqirements.txt

def ascii_art():
    art_1 = art("coffee")  # return art as str in normal mode
    print("a coffee cup for u", art_1)
    # Return ASCII text (default font) and default chr_ignore=True
    Art = text2art("art")
    print(Art)
    # Return ASCII text with block font
    Art = text2art("art", font='block', chr_ignore=True)
    print(Art)
    Art = text2art("test", "rand")  # random font mode
    print(Art)

os.chdir("src")
r = Runner(save("xv6.out"))
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(5)
    @number("1")
    def test_add_with_pointers():
        """warmup, add with pointers"""
        r.run_qemu(shell_script(['warmup 1']))
        r.match("^test_add_with_pointers\\(\\d+\\): OK\.",
                no=[".*Assertion FAILED.*"])

    @weight(5)
    @number("2")
    def test_ensure_correct_order():
        """warmup, ensure correct order"""
        r.run_qemu(shell_script(['warmup 2']))
        # In here, given the way the regex matching is happening (line by line), we
        # must provide a regex for each line that we'd like to match. If a regex 
        # matches more than one line, then it won't work because they will remove it
        # from the list. 
        r.match("^test_ensure_correct_order\\(\\d+\\): OK\.",
                no=[".*Assertion FAILED.*"])

    @weight(10)
    @number("3")
    def test_special_equals():
        """warmup, special equals"""
        r.run_qemu(shell_script(['warmup 3']))
        r.match("^test_special_equals\\(\\d+\\): OK\.",
                no=[".*Assertion FAILED.*"])

    @weight(10)
    @number("4")
    def test_string_with_q():
        """warmup, string with q"""
        r.run_qemu(shell_script(['warmup 4']))
        r.match("^test_string_with_q\\(\\d+\\): OK\.",
                no=[".*Assertion FAILED.*"])

    @weight(2)
    @number("5")
    def test_sleep_no_args():
        """sleep, no arguments"""
        r.run_qemu(shell_script(['sleep']))
        r.match(no=["exec .* failed", "$ sleep\n$"])

    @weight(3)
    @number("6")
    def test_sleep_returns():
        """sleep, returns"""
        r.run_qemu(shell_script(['sleep', 'echo OK']))
        r.match("^OK$", no=["exec .* failed", "$ sleep\n$"])

    @weight(15)
    @number("7")
    def test_sleep():
        """sleep, makes syscall"""
        r.run_qemu(shell_script(['sleep 10', 'echo FAIL']),
                stop_breakpoint('sys_sleep'))
        r.match("\\$ sleep 10", no=['FAIL'])

    @weight(20)
    @number("8")
    def test_arraylist():
        """arraylist, all"""
        r.run_qemu(shell_script(['arraylist']))
        r.match(".*OK.", no=[".*Assertion FAILED.*"])

    @weight(20)
    @number("9")
    def test_find_curdir():
        """find, in current directory"""
        fn = random_str()
        r.run_qemu(shell_script([
            'echo > %s' % fn,
            'find . %s' % fn
        ]))
        r.match('\./%s' % fn)

    @weight(10)
    @number("10")
    def test_find_recursive():
        """find, recursive"""
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



if __name__ == '__main__':
    unittest.main()
