import os
import re
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *

os.chdir("src")


# os.system("apt install cowsay")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_make_grade(self):
        """autograder us1tests.c tests"""
        print(text2art("simple shell", "rand"))
        print("====================")
        print("NOTE: bc python is dumb this will not look nice but still will be correct")
        print("====================")
        os.system("make")
        os.system("cat input.txt | ./simpleshell > output.txt")

        f = open("output.txt")
        result = f.read()
        result = result.split('\n')
        f.close()

        result_arr = []
        for i in range(len(result)):
            if "RHSH" not in result[i]:
                result_arr.append(result[i])

        for i in result_arr:
            print(i)

        # testing for zombies
        process = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE, encoding='UTF-8')
        zombie_result, error = process.communicate()
        print("========checking for zombies============")
        print(zombie_result)
        if "simpleshell" in zombie_result or "donothing" in zombie_result:
            self.assertTrue(False, "simpleshell or donothing is a zombie and did not exit")

        print("========other tests============")
        lines = [i for i, l in enumerate(result_arr) if "uwu" in l]

        print("checking for simpleshell")
        found_simpleshell = False
        print("simpleshell PID:", result_arr[lines[0] + 1])
        if result_arr[lines[0] + 1]:
            print("found simpleshell")
            found_simpleshell = True
        self.assertTrue(found_simpleshell, "simpleshell did not run")

        print("checking for donothing")
        found_donothing = False
        print("donothing PID:", result_arr[lines[1] + 1])
        if result_arr[lines[1] + 1]:
            print("found do nothing")
            found_donothing = True
        self.assertTrue(found_donothing, "donothing did not run")

        print("checking for donothing zombie")
        print("donothing PID:", result_arr[lines[2] + 1])
        if result_arr[lines[2] + 1]:
            print("found zombie")
            self.assertTrue(False, "found zombie")
        # self.assertTrue('exit' in result)


if __name__ == '__main__':
    unittest.main()
