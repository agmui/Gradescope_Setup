import os, re
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *

os.system("sudo apt install -y psmisc>/dev/null")
os.system("tar xf exam1.tar")

os.chdir("src")


class TestIntegration(unittest.TestCase):
    def setUp(self):
        print()
        print(text2art("Exam 1", "rand"))
        print()

    @weight(0)
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        os.system("gcc -o prodcon.bin prodcon.c")
        process = subprocess.Popen(['./prodcon.bin'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        reg = r'Master Process \(PID \d+\) finished\.'
        result_arr=result.split('\n')
        self.assertTrue(re.match(reg, result_arr[-2]))


if __name__ == '__main__':
    unittest.main()
