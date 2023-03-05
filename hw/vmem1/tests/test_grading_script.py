import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
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


os.chdir("cd ../src")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

# Step 1: manages to catch segfaults 	20
# Step 1: works correctly and matches output 	40
# Step 2: produces some files 	15
# Step 2: seems to be swapping pages in and out but not with FIFO algorithm 	15
# Step 2: works correctly and matches output 	50
    @weight(0)
    @number("1")
    def test_output(self):
        """autograder output tests"""
        os.system("pagedforth > testout.txt")
        
        process = subprocess.Popen(['diff .finaloutput.txt testout.txt'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)


if __name__ == '__main__':
    unittest.main()