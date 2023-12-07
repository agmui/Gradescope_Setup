import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    # getting xv6 and moving it into src
    os.system('svn export https://github.com/rhit-csse332/csse332-labs/trunk/xv6-riscv/')
    os.system('mv -f ./xv6-riscv/{.,}* /autograder/source/src/') # moves everything including hidden files

    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
