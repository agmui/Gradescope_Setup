import os.path
from .bcolors import *

SUBMISSION_BASE = '/autograder/submission/'


def submitted_files(files_to_check: list[str], base=SUBMISSION_BASE) -> int:
    """

    :param files_to_check: list of files to check it exists in /autograder/submission/ or base
    :param base: location of where the file check is happening Default /autograder/submission
    :return: number files missing
    """
    missing_files = len(files_to_check)

    # r=fullpath, d=directories, f=files
    for r, d, f in os.walk(base):  # os.walk returns list of directory and files
        file_relative_path = r.replace(base, '')  # removes the first part of the full path
        for file in f:
            file_joined_path = os.path.join(file_relative_path, file)  # adds the remaking part of the path
            if file_joined_path in files_to_check:  # check if the file is needed
                print(f"{OKGREEN}found: {file}{ENDC}")
                files_to_check.remove(file_joined_path)
                missing_files -= 1
            else:
                print(f"{WARNING}????: {file_joined_path}{ENDC}")
    for file in files_to_check:
        print(f'{FAIL}MISSING: {file}{ENDC}')

    print('---')
    print(f'{BOLD}{OKCYAN}missing {missing_files} files{ENDC}\n')

    print("if this autograder breaks pleas email/text on teams: muian@rose-hulman.edu and tell them they are and idiot\n"
          "(for example this case right here)")

    if missing_files == 0:
        print(f'\n{OKGREEN}All required files submitted!!{ENDC}')
    return missing_files


# TODO: support args or make it a decorator
def capture_output(func, *args, **kwargs):
    """
    Captures all print/stdout from given function and returns it in a buffer and whether the function crashed

    :param func: function to capture the output of
    :return: output of function and exception if there was any
    """
    import io
    from contextlib import redirect_stdout

    # Create an in-memory buffer to capture output
    buffer = io.StringIO()
    err = None
    with redirect_stdout(buffer):
        """
        Note: in gradelib.py there already is a try: except: statement for the students code
        making the try except here redundant. However gradelib.py also exit(1) if not all
        the test cases pass. So for redirect_stdout to work we need a try: except: and
        changing gradelib.py will make the gradescope environment different from the students
        so we are forced to have two try: except: blocks.
        """
        try:
            func(*args, **kwargs)  # Call the original function
        except BaseException as error:
            print(f"{FAIL}--test crashed--{ENDC}")
            print(f"{FAIL}error/return code:{ENDC}\n {error}")
            print(f"{FAIL}----------------{ENDC}")
            err = error

    return buffer.getvalue(), err
