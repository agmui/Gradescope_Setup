import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    print("==================== run_tests.py ====================")
    # getting xv6 and moving it into src
    os.system('svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/')
    os.system('mv ./xv6-riscv/ /autograder/source/src/')

    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
