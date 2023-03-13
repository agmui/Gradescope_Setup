import os
import re
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *

os.chdir("src")

# ================= preprocess =============
print("hlep")
os.system("apt install -y cowsay")
os.system("echo test | cowsay")

result_arr = []
f = open("output.txt")
result = f.read()
print(result)
result = result.split('\n')
f.close()

for i in range(len(result)):
    if "RHSH" not in result[i]:
        result_arr.append(result[i])

print("==================== output ==================== ")
for i in result_arr:
    print(i)
print("======================================== ")

lines = [i for i, l in enumerate(result_arr) if "uwu" in l or "Background" in l]
# ====================================


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    def test_idk(self):
        """checking is simpleshell even ran"""
        print(text2art("simple shell", "rand"))
        print("====================")
        print("NOTE: bc python is dumb this will not look nice but still will be correct")
        print("====================")

        print("checking for simpleshell")
        found_simpleshell = False
        print("simpleshell PID:", result_arr[lines[0] + 1])
        if result_arr[lines[0] + 1]:
            print("found simpleshell")
            found_simpleshell = True
        self.assertTrue(found_simpleshell, "simpleshell did not run")

    # @weight(0)
    # @number("1")
    # def test_foreground_cmd(self):
    #     """foreground commands"""
    #     self.assertTrue("run: \"rm -rf \\" in result_arr[1], "did not run foreground cmd")

    @weight(0)
    @number("2")
    def test_background_cmd(self):
        """background commands"""
        print("checking for donothing")
        found_donothing = False
        print("donothing PID:", result_arr[lines[1] + 1])
        if result_arr[lines[1] + 1]:
            print("found do nothing")
            found_donothing = True
        self.assertTrue(found_donothing, "donothing did not run")

    @weight(0)
    @number("3")
    def test_background_notification(self):
        """background notification"""
        self.assertTrue(len(lines) == 4, "no background notification")

    @weight(0)
    @number("4")
    def test_zombie(self):
        """zombie"""
        # testing for zombies after running shell
        process = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE, encoding='UTF-8')
        zombie_result, error = process.communicate()
        print("========checking for zombies============")
        print(zombie_result)
        if "simpleshell" in zombie_result or "donothing" in zombie_result:
            self.assertTrue(False, "simpleshell or donothing is a zombie and did not exit")

        # testing for zombies while shell is running
        print("checking for donothing zombie")
        print("donothing PID:", result_arr[lines[3] + 1])
        if result_arr[lines[3] + 1]:
            print("found zombie")
            self.assertTrue(False, "found zombie")


if __name__ == '__main__':
    unittest.main()
