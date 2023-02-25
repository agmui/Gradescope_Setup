import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number



class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    def test_us1tests(self):
        """autograder integration tests"""
        process = subprocess.Popen(['./semgrep --config rule.yaml'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue("OK" in result)


if __name__ == '__main__':
    unittest.main()
