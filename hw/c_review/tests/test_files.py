import os.path
import unittest
from gradescope_utils.autograder_utils.decorators import weight
from gradescope_utils.autograder_utils.files import check_submitted_files
import glob


class TestFiles(unittest.TestCase):
    @weight(0)
    def test_submitted_files(self):
        """Check submitted files"""
        # missing_files = check_submitted_files([
        #     'submission-*.zip'
        #     #'submit-lab-0.tar','submit-lab-0.patch'
        #     ])
        SUBMISSION_BASE = '/autograder/submission'
        files_to_check = ['arraylist.c', 'find.c', 'sleep.c', 'warmup.c']  # TODO: check for extra files
        missing_files = []
        for file in files_to_check:
            if len(glob.glob(os.path.join(SUBMISSION_BASE, file))) == 0:
                missing_files.append(file)
        for path in missing_files:
            print('Missing {0}'.format(path))
        self.assertEqual(len(missing_files), 0, 'Missing some required files!')
        print('All required files submitted!')
