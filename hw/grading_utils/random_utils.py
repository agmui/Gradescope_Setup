import os.path
import glob

def submitted_files(files_to_check):
    """Check submitted files"""
    SUBMISSION_USER_BASE = '/autograder/submission/user'
    # files_to_check = ['arraylist.c', 'find.c', 'sleep.c', 'warmup.c']  # TODO: check for extra files
    missing_files = 0
    for file in files_to_check:
        #TODO: remove unwanted files so gradescope will show less
        # TODO: show/print which files read/submitted
        if len(glob.glob(os.path.join(SUBMISSION_USER_BASE, file))) == 0:
            print(f'Missing {file}')  # .format(path))
            missing_files += 1
        else:
            print('found:', file)
    return missing_files
    # self.assertEqual(missing_files, 0, 'Missing some required files!')

# Define a wrapper function to capture the output
def capture_output(func):
    import io
    from contextlib import redirect_stdout

    # Create an in-memory buffer to capture output
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()  # Call the original function

    return buffer.getvalue()