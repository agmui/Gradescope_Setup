import os
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
# NOTE: this code will not be shown to the students and only to the grader
print("uwu") 

os.chdir("src") # to change to the right folder
class TestIntegration(unittest.TestCase):
    def setUp(self):
        # this function runs at the start of every test
        pass

    @weight(0) # number of points when test passes
    @visibility('hidden') # to hide from students
    def test_example_one(self):
        """this comment is the name that will be displayed in gradescope"""

        # don't worry about this ;)
        print(text2art("heap manager", "rand")) 

        # checking solution
        # the second argument is what gets displayed to the student when the solution is wrong
        self.assertTrue(True, "If you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0")

    @weight(0) # number of points when test passes
    # note you don't always need to hide tests
    def test_example_two(self):
        """autograder uwu tests"""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
