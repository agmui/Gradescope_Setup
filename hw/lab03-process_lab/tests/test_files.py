import unittest
import sys
from gradescope_utils.autograder_utils.decorators import weight
sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.random_utils import submitted_files


class TestFiles(unittest.TestCase):
    @weight(0)
    def test_submitted_files(self):
        """Check submitted files"""
        missing_files = submitted_files(['simple_test.c'])
        self.assertEqual(missing_files, 0, 'Missing some required files!')
        print('All required files submitted!!')
