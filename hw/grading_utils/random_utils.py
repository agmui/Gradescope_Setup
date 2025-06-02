import json
import os.path

import random
from art import text2art
from .bcolors import *

SUBMISSION_BASE = '/autograder/submission/'
SUBMISSION_METADATA = '/autograder/submission_metadata.json'


def submitted_files(files_to_check: list[str], base=SUBMISSION_BASE) -> int:
    """

    :param files_to_check: list of files to check it exists in /autograder/submission/ or base
    :param base: location of where the file check is happening Default /autograder/submission
    :return: number files missing
    """
    with open(SUBMISSION_METADATA, 'r') as f:

        links = [
            "https://www.youtube.com/watch?v=xvFZjo5PgG0",
            "https://mrdoob.com/#/157/spin_painter",
            "https://www.youtube.com/watch?v=Q591qHMJgSI",
            "https://www.youtube.com/watch?v=LaGP-CVfENQ",
            "https://docs.google.com/forms/d/e/1FAIpQLSfhQQLJKwMup5vkAd9BBnEZTGOpYZHjvfSJg8V4YlQKp9TufA/viewform",
            "https://blueballfixed.ytmnd.com/",
            "https://theuselessweb.com/",
            """
                    --------------------
                    --- Please go to ---
                    --------------------
                    https://forms.gle/1arfiPaZPcCGAavb7
                    note: it is not a rick roll this time it is a very important poll
                    --------------------

                    LIVE DATA:
                    Q: Is pineapple on pizza the Morally correct
                    53.1% yes   46.9% no
                    -------
                    Q: Gas station sushi?
                    53.1% yes   49.9% no
            """,
        ]

        submission_metadata = json.load(f)
        assignment_title: str = submission_metadata["assignment"]["title"]

        output = text2art(assignment_title, "rand") + f"""
        {BOLD}{FAIL}===========!!!WARNING YOU ARE NOT DONE!!!=========={ENDC}
        
         please go to this link to turn in the assignment:
         {OKBLUE}{random.choice(links)}{ENDC}
        
        {BOLD}{FAIL}==================================================={ENDC}
        """
        print(output)

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

def editOutput(json_data):
    with open(SUBMISSION_METADATA, 'r') as f:
        submission_metadata = json.load(f)
        assignment_title: str = submission_metadata["assignment"]["title"]

        github_link = "https://raw.githubusercontent.com/agmui/Gradescope_Setup/refs/heads/main/img/autograder_images/"
        image_list = [
            (("review",), github_link+"linux_example.png"),
            (("shell",), github_link+"vim_example.jpg"),
            (("process","child","parent"), github_link+"process_example.png"),
            (("heap",), github_link+"heap_example.png"),
            (("copy-on-write", "copy on write","cow"), github_link+"heap2_example.jpeg"),
            (("threads", "mutex"), github_link+"pthreads_example.jpg"),
            (("basics", "cond", "condition", "variables"), github_link + "mutex_example.jpg"),
            (("cond", "condition", "variables"), github_link + "deadlock_example.jpg"),
            (("scheduler", "sched"), github_link + "scheduler_example.jpeg"),
            (("ext2", "filesystem", "file system"), github_link + "ext_example.png"),
        ]

        """
        scans if any substring in image list is in assignment title and returns
        associated image link
        """
        def get_link():
            for img_tuple in image_list:
                for candidate in img_tuple[0]:
                    if candidate in assignment_title.casefold():
                        return img_tuple[1]
            else:
                return random.choice(image_list)[1] #image_list[randint() % len(image_list)][1]
        img_link = get_link()


        for i in ("threads", "mutex"):
            if i in assignment_title.casefold():
                dir_path = os.path.dirname(os.path.realpath(__file__))
                with open(dir_path+"/face.txt",'r') as face:
                    json_data["tests"].insert(1, {
                        "status": "passed",
                        "output":
                            face.read()+
                            text2art('''
                If you change
                global var before
                locking...
                I will come for you
                in your sleep  >:)'''),
                            "output_format": "ansi"
                    })
        json_data["tests"].insert(1, { # inserts image as base64 format
            "status": "passed",
            # "output": '<img alt="tux" src="/autograder/hw/grading_utils/Tux.svg.png">',
            "output": f'<h1>Weekly OS memes:</h1>\n<img width="400" alt="tux" src="{img_link}">',
            "output_format": "html"
        })

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
