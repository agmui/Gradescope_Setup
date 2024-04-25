import sys
from multiprocessing import Process, Queue
import os
import re
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *

sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.random_utils import capture_output

os.chdir("src")


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # print("if you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help\n")
        pass

    def run_program(self, program, str_input, div_num, n):
        input_str = f'./{program} {str_input} {div_num} {n}'
        print(f'== running: {input_str} ==\n')
        rez = subprocess.run(input_str.split(), capture_output=True, text=True, timeout=10)
        print(rez.stdout,'\n')
        if(len(re.findall('Start', rez.stdout))!= div_num):
            print('ERROR: not the right number of Start messages')
        if(len(re.findall('End', rez.stdout))!= div_num):
            print('ERROR: not the right number of End messages')
        if(re.search('problem finished', rez.stdout) == None):
            print('ERROR: no problem finished msg')

    @weight(0)
    @number("1")
    def test_problem1(self):
        """problem1"""
        q = Queue()
        inputs_arr = [('problem1.bin', 'abcdefgh', 4, 4),
                      ('problem1.bin', 'aaaa', 4, 5),
                      ('problem1.bin', 'a', 1, 4),
                      ('problem1.bin', 'deadbeef', 8, 4)]

        jobs = [Process(target=lambda q, args: q.put(capture_output(self.run_program, *args)),
                        args=(q, i)) for i in inputs_arr]

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
            print(q.get()[0])


    @weight(0)
    @number("2")
    def test_problem2(self):
        """problem2"""
        # print('running: ./problem2.bin abcdefgh 4 4\n')
        # rez = subprocess.run('./problem1.bin abcdefgh 4 4'.split(), capture_output=True, text=True)
        # print(rez.stdout)
        # self.assertTrue(True)

        q = Queue()
        inputs_arr = [('problem2.bin', 'abcdefgh', 4, 4),
                      ('problem2.bin', 'a', 1, 4),
                      ('problem2.bin', 'deadbeef', 8, 4)]

        jobs = [Process(target=lambda q, args: q.put(capture_output(self.run_program, *args)),
                        args=(q, i)) for i in inputs_arr]

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
            print(q.get()[0])

    @weight(0)
    @number("3")
    def test_problem3(self):
        """problem3"""
        # print('running: ./problem3.bin abcdefghij 5 3\n')
        # rez = subprocess.run('./problem1.bin abcdefghij 5 3'.split(), capture_output=True, text=True)
        # print(rez.stdout)
        # self.assertTrue(True)


        q = Queue()
        inputs_arr = [('problem3.bin', 'abcdefghij', 5, 3),
                      ('problem3.bin', 'abcdefgh', 4, 4),
                      ('problem3.bin', 'a', 1, 4),
                      ('problem3.bin', 'deadbeef', 8, 4)]

        jobs = [Process(target=lambda q, args: q.put(capture_output(self.run_program, *args)),
                        args=(q, i)) for i in inputs_arr]

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
            print(q.get()[0])


if __name__ == '__main__':
    unittest.main()
