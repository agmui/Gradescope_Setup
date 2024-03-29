import os
import sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility

# sys.path.insert(0, '../..')  # adds the hw project dir to the python path

# from hw.grading_utils.integrationlib import test_run

# os.chdir("src")

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @visibility('hidden')
    def test_arraylist(self):
        """autograder integration test"""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
