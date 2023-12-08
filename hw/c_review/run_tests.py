import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    # getting xv6 and moving it into src
    # os.system('svn export https://github.com/rhit-csse332/csse332-labs/branches/clab/xv6-riscv/ > /dev/null')
    # os.system('mv ./xv6-riscv/ /autograder/source/src/')
    # os.system("mv /autograder/source/src/user/*.c /autograder/source/src/xv6-riscv/user/")  # FIXME:
    # os.system("make > /dev/null")

    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
