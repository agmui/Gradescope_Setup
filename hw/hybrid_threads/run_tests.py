import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

cmd = "svn export \"https://github.com/agmui/gradescope_semgrep/trunk/hybrid_threads\""
os.system(cmd)
os.system("cp -r hybrid_threads/* .")

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
