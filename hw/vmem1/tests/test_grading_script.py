import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt


os.chdir("src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_output(self):
        """autograder output tests"""
        print(text2art("stack smashing", "rand"))
        print("if the autograder does not work email muian@rose-hulman.edu and tell them they are an idiot and tell them to fix it\n")
        os.system("make")
        os.system("./pagedforth > testout.txt")
        
        process = subprocess.Popen(['diff finaloutput.txt testout.txt'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)


if __name__ == '__main__':
    unittest.main()
