import unittest
from gradescope_utils.autograder_utils.decorators import weight
from gradescope_utils.autograder_utils.files import check_submitted_files
import glob
import os.path

class TestFiles(unittest.TestCase):
    @weight(0)
    def test_submitted_files(self):
        """Check submitted files"""
        SUBMISSION_USER_BASE = '/autograder/submission/user'
        files_to_check = ['rhmalloc.c']  # TODO: check for extra files
        missing_files = 0
        for file in files_to_check:
            if len(glob.glob(os.path.join(SUBMISSION_USER_BASE, file))) == 0:
                print(f'Missing {file}')  # .format(path))
                missing_files += 1
        self.assertEqual(missing_files, 0, 'Missing some required files!')
        print('All required files submitted!')
        # missing_files = check_submitted_files(['submit-lab-1.tar','submit-lab-1.patch'])
        # for path in missing_files:
        #     print('Missing {0}'.format(path))
        # self.assertEqual(len(missing_files), 0, 'Missing some required files!')
        # print('All required files submitted!')
