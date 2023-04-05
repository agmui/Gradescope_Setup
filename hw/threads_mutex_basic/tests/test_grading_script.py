import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *


os.chdir("src")
os.system("gcc -pthread -ggdb factoring.c -o thread_factoring.bin")
os.system("gcc -pthread -ggdb threadSort.c -o thread_sort.bin")
os.system("gcc -pthread -ggdb add_a_lot.c -o basic_mutex.bin")
os.system("gcc -pthread -ggdb red_blue_purple.c -o red_blue_purple.bin")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        print("if you have questions go to: https://www.youtube.com/watch?v=xvFZjo5PgG0 for help")

    @weight(0)
    @number("1")
    def test_thread_factoring(self):
        """autograder us1tests.c tests"""
        f = open('../tests/face.txt')
        print(f.read())
        f.close()
        print(text2art('''
        If you change a
        global var before
        locking...
        I will come for you
        in your sleep'''))
        process = subprocess.Popen(['./thread_factoring.bin'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue(True)
    def test_thread_sorting(self):
        process = subprocess.Popen(['./threadSort.bin'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue(True)
    def test_basic_mutex(self):
        process = subprocess.Popen(['./basic_mutex.bin'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue(True)

    def test_ReadBluePurple(self):
        process = subprocess.Popen(['./red_blue_purple.bin'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print(result)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
