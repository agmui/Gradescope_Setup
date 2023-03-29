import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *


os.chdir("src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        # print("If you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help")
        pass

    @weight(0)
    @number("1")
    def test_output(self):
        """autograder output tests"""
        print(text2art("stack smashing", "rand"))
        print("--------------------")
        print("--- Please go to ---")
        print("--------------------")
        print("https://forms.gle/1arfiPaZPcCGAavb7")
        print("note: it is not a rick roll this time it is a very important poll")
        print("--------------------\n")
        print("LIVE DATA:")
        print("Q: Is pineapple on pizza the Morally correct")
        print("66.67% yes   33.3% no")
        print("-------")
        print("Q: Gas station sushi?")
        print("66.67% yes   33.3% no")
        os.system("make")
        os.system("./pagedforth > testout.txt")
        
        process = subprocess.Popen(['diff', 'finaloutput.txt', 'testout.txt'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        # print(result)
        self.assertTrue("done" in result)


if __name__ == '__main__':
    unittest.main()
