import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    os.chdir("src/csse332-labs/xv6-riscv")
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
