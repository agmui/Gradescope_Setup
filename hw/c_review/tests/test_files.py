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
        SUBMISSION_USER_BASE = '/autograder/submission/user'
        files_to_check = ['arraylist.c', 'find.c', 'sleep.c', 'warmup.c']  # TODO: check for extra files
        missing_files = 0
        for file in files_to_check:
            if len(glob.glob(os.path.join(SUBMISSION_USER_BASE, file))) == 0:
                print(f'Missing {file}')  # .format(path))
                missing_files += 1
        self.assertEqual(missing_files, 0, 'Missing some required files!')
        print('All required files submitted!')
