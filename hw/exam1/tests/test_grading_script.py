import os
import re
import subprocess
import unittest

from gradescope_utils.autograder_utils.decorators import weight, number

os.chdir('src')


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    def test_make_problem(self):
        """Processing files"""

        process = subprocess.Popen("./processbatch.bin 1.txt 2.txt 3.txt 4.txt 5.txt".split(),
                                   bufsize=0,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   encoding='UTF-8',
                                   # shell=True
                                   )
        result, error = process.communicate()

        print(result)
        print(error)
        self.assertTrue(len(result))


if __name__ == '__main__':
    unittest.main()
