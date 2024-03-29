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
    def test_problem3(self):
        """problem 3"""

        #TODO: cant use communicat for some reason

        # process = subprocess.Popen("./problem3.bin".split(),
        #                            stdout=subprocess.PIPE,
        #                            stderr=subprocess.STDOUT,
        #                            encoding='UTF-8',
        #                            # shell=True
        #                            )
        # result, error = process.communicate(input="100\n")
        #
        # print(result)
        # print(error)
        # self.assertTrue(len(result))
        with open('problem3_rez.txt','r') as f:
            print(f.read())

    @weight(0)
    def test_problem4(self):
        """problem 4"""

        # process = subprocess.Popen("./problem4_parent.bin".split(),
        #                            stdout=subprocess.PIPE,
        #                            stderr=subprocess.STDOUT,
        #                            encoding='UTF-8',
        #                            # shell=True
        #                            )
        # result, error = process.communicate(input="10\n")
        #
        # print(result)
        # print(error)
        # self.assertTrue(len(result))
        with open('problem4_rez.txt','r') as f:
            print(f.read())


if __name__ == '__main__':
    unittest.main()
