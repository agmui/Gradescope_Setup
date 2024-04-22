import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *

os.chdir("src")

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # print("if you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help\n")
        pass

    @weight(0)
    @number("1")
    def test_problem1(self):
        """problem1"""
        # process = subprocess.Popen(['./thread_factoring.bin'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                            encoding='UTF-8')
        # result, error = process.communicate(input="143\n2") #TODO: add timeouts

        print('./problem1.bin abcdefgh 4 4')
        subprocess.run('./problem1.bin abcdefgh 4 4'.split(), stdout=subprocess.STDOUT)
        print('./problem2.bin abcdefgh 4 4')
        subprocess.run('./problem2.bin abcdefgh 4 4'.split(), stdout=subprocess.STDOUT)
        print('./problem3.bin abcdefghij 5 3')
        subprocess.run('./problem3.bin abcdefghij 5 3'.split(), stdout=subprocess.STDOUT)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
