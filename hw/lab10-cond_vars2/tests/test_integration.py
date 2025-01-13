import subprocess
import re, os
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility




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
