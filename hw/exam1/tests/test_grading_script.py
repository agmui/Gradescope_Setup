import os
import re
import subprocess
import unittest

from art import *
from gradescope_utils.autograder_utils.decorators import weight, number

os.system("apt -y update > /dev/null")
os.system("apt -y upgrade > /dev/null")
os.system("apt install -y psmisc > /dev/null")
os.chdir("src")
os.system("tar xf exam1.tar")


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    def test_make_problem(self):
        """make_problem"""
        print()
        print(text2art("Exam One", "rand"))
        print()
        os.chdir("make_problem")
        os.system("make clean")
        os.system("make")
        file_name = "./main"
        if os.path.exists('./main.bin'):
            file_name = './main.bin'
        process = subprocess.Popen([file_name], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        os.chdir("../")
        self.assertTrue("─────────▀▀▀▀────────▀▀▀▀" in result)

    @weight(0)
    def test_prodcon(self):
        """prodcon.c test"""
        os.system("gcc -o prodcon.bin prodcon.c")
        process = subprocess.Popen(['./prodcon.bin'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        reg = r'Master Process \(PID \d+\) finished\.'
        result_arr = result.split('\n')
        self.assertTrue(re.match(reg, result_arr[-2]))


if __name__ == '__main__':
    unittest.main()
