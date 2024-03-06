import unittest
import sys
from gradescope_utils.autograder_utils.decorators import weight
sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.files_check import submitted_files


class TestFiles(unittest.TestCase):
    @weight(0)
    def test_submitted_files(self):
        """Check submitted files"""
        missing_files = submitted_files(['arraylist.c', 'find.c', 'sleep.c', 'warmup.c'])
        self.assertEqual(missing_files, 0, 'Missing some required files!')
        print('All required files submitted!')

        # SUBMISSION_USER_BASE = '/autograder/submission/user'
        # files_to_check = ['arraylist.c', 'find.c', 'sleep.c', 'warmup.c']  # TODO: check for extra files
        # missing_files = 0
        # for file in files_to_check:
        #     #TODO: remove unwanted files so gradescope will show less
        #     # TODO: show/print which files read/submitted
        #     if len(glob.glob(os.path.join(SUBMISSION_USER_BASE, file))) == 0:
        #         print(f'Missing {file}')  # .format(path))
        #         missing_files += 1
        #     else:
        #         print('found:', file)
        # self.assertEqual(missing_files, 0, 'Missing some required files!')
        # print('All required files submitted!')
