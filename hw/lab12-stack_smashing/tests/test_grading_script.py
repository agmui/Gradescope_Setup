import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt

# os.system("apt update -y > /dev/null && apt upgrade -y > /dev/null")
# os.system("apt install -y gdb gdb-multiarch gcc-multilib python2")
# os.system("bash -c \"$(curl -fsSL https://gef.blah.cat/sh)\"")
os.chdir("src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder dummy tests"""
        # process = subprocess.Popen(['./part8 $(python2 part8.py)'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        # print(result)

        output_str = """
        --------------------
        --- Please go to ---
        --------------------
        https://forms.gle/1arfiPaZPcCGAavb7
        note: it is not a rick roll this time it is a very important poll
        --------------------

        LIVE DATA:
        Q: Is pineapple on pizza the Morally correct
        59.1% yes   40.9% no
        -------
        Q: Gas station sushi?
        54.5% yes   45.5% no
        """
        print(output_str)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
