import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio  # TODO: add to reqirements.txt
import re

os.chdir("src/csse332-labs/ext2")


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_testcode(self):
        """autograder testcode tests"""
        process = subprocess.Popen('valgrind --log-fd=1 --leak-check=yes ./testcode 451_filesystem.ext2'.split(), stdout=subprocess.PIPE,
                                   encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue(True)
        process.terminate()#TODO: add terminate to all subprocessPopen
    @weight(0)
    @number("2")
    def test_filereader(self):
        """autograder file reader tests"""
        process = subprocess.Popen('./filereader 451_filesystem.ext2 /small-file.txt'.split(), stdout=subprocess.PIPE,
                                   encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertEqual("file at inode 15\noutputing file named small-file.txt...\n", result)
        process.terminate()#TODO: add terminate to all subprocessPopen
    # TODO: add valgrind test


if __name__ == '__main__':
    unittest.main()
