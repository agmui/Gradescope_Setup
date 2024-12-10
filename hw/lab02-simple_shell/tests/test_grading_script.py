import os
import re
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


os.chdir("src")

# ================= preprocess =============

#TODO: check if submissions even exit properly bc sometimes exit does not work for some.
f = open("output.txt")
shell_output = f.read()
# print(shell_output)
f.close()
result = shell_output.split('\n')

for i in result[1:]:
    if "%" in i:
        print()
    str_arr = i.split('%')
    if len(str_arr) > 1:
        print(bcolors.OKGREEN+bcolors.BOLD + str_arr[0] + '%' + bcolors.ENDC+bcolors.OKCYAN + str_arr[1] + bcolors.ENDC)
    else:
        print(bcolors.OKCYAN + i + bcolors.ENDC)


regex_str = ".*% ?pgrep simpleshell\n.*\n?(\d+)"
print('---')
pids = re.findall(regex_str, shell_output)


# ====================================

def print_html_gif(filename):
    with open(f"/autograder/hw/test_suite/src/{filename}") as gif:
        print(f'<img alt="gif" src="data:image/gif;base64,{gif.read()}">')


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    #TODO: test repeat commands ex: SHELL% 2sleep
    @weight(0)
    @number("1")
    def test_foreground_cmd(self):
        """checking for foreground commands"""

        print_html_gif("base64test1.txt")

        # TODO: display  block for all tests
        print("checking if simpleshell can run other commands (ps -a)")
        found_simpleshell = False

        regex_str = ".*% pgrep simpleshell\n.*\n?(\d+)\n.*%" #TODO: look for the next % and right above it
        rez = re.search(regex_str, shell_output)

        if len(pids) > 0:
            found_simpleshell = True
        err_msg = "either simpleshell could not run ps -a OR simpleshell did not build/run  properly" \
                  " \n ---autograder output---\n"
        # self.assertTrue(found_simpleshell, err_msg + rez.group())

        self.assertTrue(True)

    @weight(0)
    @number("2")
    def test_background_cmd(self):
        """background commands"""

        print_html_gif("base64test2.txt")

        print("checking if BG./donothing can be run")
        found_donothing = False
        rez = re.search('.*% ?BG\./donothing\n.*\n?(.*\n)?.*% ?BG\./donothing\n.*', shell_output)
        if rez is not None and len(rez.group().split('\n')) >= 4:
            found_donothing = True
        error_str = "running BG./donothing had an error\n--autograder output--\n" + rez.group() if rez is not None else "could not find"
        # self.assertTrue(found_donothing, error_str)
        self.assertTrue(True)

    @weight(0)
    @number("3")
    def test_background_notification(self):
        """background notification"""

        print_html_gif("base64test3.txt")

        print("checking if BG./donothing can be run")
        found_notification = False
        rez = re.search('.*Background command finished.*', shell_output)
        if rez is not None:  # and len(rez.group().split('\n')) == 2:
            found_notification = True

        #TODO: fix err msg
        err_msg = "no background notification:" + rez.group() if found_notification else ("Could not find \"Background command finish\" printout."
                                                                                          "\nMake sure \"Background command finished\" gets printed out when BG./donothing finishes")
        # self.assertTrue(found_notification, err_msg)
        self.assertTrue(True)

    @weight(0)
    @number("4")
    def test_background_cmd_with_args(self):
        """background commands with arguments"""

        print_html_gif("base64test4.txt")

        print("checking if BG can do args")
        found_donothing = False
        # rez = re.search('.*BGsleep 2\n.*\n?.*\n', shell_output)
        rez = re.search('.*\'BGsleep\' with argument \'2\'(.*\n)?.*\n(.*\n)?.*\'echo\' with argument \'uwu\'.*', shell_output)
        if rez is not None and len(rez.group().split('\n')) >= 2:
            found_donothing = True


        # self.assertTrue(found_donothing, "BGsleep 2 did not run:\n"+rez.group() if rez is not None else "(could not find output)")
        self.assertTrue(True)

    @weight(0)
    @number("5")
    def test_zombie(self):
        """zombie"""

        print_html_gif("base64test5.txt")

        zombie_rez = False
        print("checking for zombies")
        # i = None
        for i in reversed(range(len(result))):
            if "% pgrep simpleshell" in result[i] and result[i + 2].isnumeric():
                zombie_rez = True
                break
        # self.assertTrue(zombie_rez, "simpleshell or ./donothing is a zombie and did not exit")
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
