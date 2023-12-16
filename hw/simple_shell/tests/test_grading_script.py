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

f = open("output.txt")
shell_output = f.read()
# print(result)
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

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    def test_foreground_cmd(self):
        """checking for foreground commands"""
        print(text2art("simple shell", "rand"))
        # print("====================")
        # print("NOTE: bc python is dumb this will not look nice but still will be correct")
        # print("====================")

        # TODO: display  block for all tests
        print("checking if simpleshell can run other commands (ps -a)")
        found_simpleshell = False

        regex_str = ".*% pgrep simpleshell\n.*\n?(\d+)"
        rez = re.search(regex_str, shell_output)
        # print(rez.group())

        # i = result.index("% pgrep simpleshell")
        if len(pids) > 0:
            found_simpleshell = True
        err_msg = "either simpleshell could not run ps -a OR simpleshell did not build/run  properly" \
                  " \n ---autograder output---\n"
        self.assertTrue(found_simpleshell, err_msg + rez.group())

    @weight(0)
    @number("2")
    def test_background_cmd(self):
        """background commands"""
        print("checking if BG./donothing can be run")
        found_donothing = False
        rez = re.search('.*% ?BG\./donothing\n.*\n?(.*\n)?.*% ?BG\./donothing\n.*', shell_output)
        if rez is not None and len(rez.group().split('\n')) >= 4:
            found_donothing = True
        # print(rez.group())
        # print("donothing PID:", pids[1])
        # if pids[1]:
        #     print("found donothing!!")
        #     found_donothing = True

        # i = result.index("Command is \'pgrep\' with argument \'donothing\'")
        # print("./donothing pids:", result[i + 1:i + 3])
        # if result[i + 1].isnumeric() and result[i + 2].isnumeric():
        #     found_donothing = True
        #     # pass

        error_str = "running BG./donothing had an error\n--autograder output--\n" + rez.group() if rez is not None else "could not find"
        self.assertTrue(found_donothing, error_str)

    @weight(0)
    @number("3")
    def test_background_notification(self):
        """background notification"""

        print("checking if BG./donothing can be run")
        found_notification = False
        rez = re.search('.*Background command finished.*', shell_output)
        if rez is not None:  # and len(rez.group().split('\n')) == 2:
            found_notification = True
        # i = result.index("Background command finished")
        # i = None
        # for index, s in enumerate(result):
        #     if "Background command finished" in s:
        #         i = index
        #         break
        # if i != None:
        #     found_notification = True
        err_msg = "no background notification:" + rez.group() if rez is not None else "could not find"
        self.assertTrue(found_notification, err_msg)

    @weight(0)
    @number("4")
    def test_background_cmd_with_args(self):
        """background commands with arguments"""
        print("checking if BG can do args")
        found_donothing = False
        # rez = re.search('.*BGsleep 2\n.*\n?.*\n', shell_output)
        rez = re.search('.*\'BGsleep\' with argument \'2\'(.*\n)?.*\n.*\'echo\' with argument \'uwu\'.*', shell_output)
        if rez is not None and len(rez.group().split('\n')) >= 2:
            found_donothing = True

        # print("donothing PID:", pids[1])
        # i = result.index("Command is \'BGsleep\' with argument \'2\'")
        # if i:
        #     print("simpleshell can do BG cmds with args!")
        #     found_donothing = True
        self.assertTrue(found_donothing, "BGsleep 2 did not run:\n"+rez.group() if rez is not None else "(could not find output)")

    @weight(0)
    @number("5")
    def test_zombie(self):
        """zombie"""

        zombie_rez = False
        print("checking for zombies")
        # i = None
        for i in reversed(range(len(result))):
            if "% pgrep simpleshell" in result[i] and result[i + 2].isnumeric():
                zombie_rez = True
                break
        self.assertTrue(zombie_rez, "simpleshell or ./donothing is a zombie and did not exit")
        # testing for zombies after running shell
        # os.system("ps -a")
        # process = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE, encoding='UTF-8')
        # zombie_result, error = process.communicate()
        # print("========checking for zombies============")
        # print(zombie_result)
        # if "simpleshell" in zombie_result or "donothing" in zombie_result:
        #     self.assertTrue(False, "simpleshell or donothing is a zombie and did not exit")

        # testing for zombies while shell is running
        # print("checking for donothing zombie")
        # print("donothing PID:", result_arr[pids[3] + 1])
        # if result_arr[pids[3] + 1]:
        #     print("found zombie")
        #     self.assertTrue(False, "found zombie")


if __name__ == '__main__':
    unittest.main()
