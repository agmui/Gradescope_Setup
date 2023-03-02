import subprocess
import re


# import unittest
# from gradescope_utils.autograder_utils.decorators import weight, tags, number

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


def ordered_pattern(file_arr, bounding_func, pattern_arr):
    # ====================  getting function scope ====================
    start_index: int = -1
    end_index: int = 0
    cur_count = 0
    for i, line in enumerate(file_arr):
        if bounding_func in line:
            start_index = i
        if start_index != -1:
            if '{' in line:
                cur_count += 1
            if '}' in line:
                cur_count -= 1
            if cur_count == 0 and start_index != i:
                end_index = i
                break

        # removing comments from file_arr
        comment_index = line.find("//")
        if comment_index != -1:
            file_arr[i] = line[:comment_index]

    # truncate file_arr to only the function scope
    file_arr = file_arr[start_index:end_index + 1]

    # ========================= substring search ========================
    format_arr = ['n'] * len(file_arr)  # for printing output
    past = 0
    line_num = 0
    for sub_str in pattern_arr:
        if not isinstance(sub_str, list):  # to wrap substring in arr
            sub_str = [sub_str]
        for comment_index in sub_str:
            for c in ['(', ')', '+', '=']:
                comment_index = comment_index.replace(c, '\\' + c)
            arr = [line for line in file_arr if re.findall(comment_index, line)]
            if len(arr) != 0:
                line_num = file_arr.index(arr[0])
                # file_arr[line_num] = ""
        if line_num < past:
            format_arr[line_num] = 'w'
        elif line_num == past:
            format_arr[line_num] = sub_str
        else:
            format_arr[line_num] = 'o'

        past = line_num

    # ========================= printing output ========================
    for i, line in enumerate(file_arr):
        match format_arr[i]:
            case 'o':
                print(f'{bcolors.OKGREEN}{start_index + i + 1:4d} | {file_arr[i]}{bcolors.ENDC}')
            case 'w':
                print(f'{bcolors.WARNING}{start_index + i + 1:4d} | {file_arr[i]} \t\t out of order{bcolors.ENDC}')
            case 'n':
                print(f'{start_index + i + 1:4d} | {file_arr[i]}')
            case _:  # error case
                print(f'{start_index + i + 1:4d} | {file_arr[i]}')
                print(bcolors.FAIL + "missing", format_arr[i], bcolors.ENDC)


# reading file into arr
file = open("../src/inorder.c")
file_arr = file.read().split('\n')
file.close()

# must define bounding function area of code is in
bounding_func = "void *thread(void *arg)"
pattern_arr = [  # wild cards are defined by .*
    "pthread_mutex_lock(.*)",
    "while(.*)",
    "pthread_cond_wait(.*)",
    [".*++;", ".*+=.*"],
    "pthread_mutex_unlock(.*)",
    ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"]
]
ordered_pattern(file_arr, bounding_func, pattern_arr)

# class TestIntegration(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     @weight(0)
#     def test_inorder_mutex(self):
#         """autograder integration tests"""
#         # self.assertTrue(inorder_result[0])
#
#     @weight(0)
#     def test_inorder_cond_var(self):
#         """autograder integration tests"""
#         # self.assertTrue(inorder_result[1])
#
#     @weight(0)
#     def test_inorder_mutex_init(self):
#         """autograder integration tests"""
#         # self.assertTrue(inorder_result[2])
#
#     @weight(0)
#     def test_inorder_thread_func(self):
#         """autograder integration tests"""
#         # self.assertTrue(inorder_result[3])
#
#     @weight(0)
#     def test_max_mutex(self):
#         """autograder integration tests"""
#         # self.assertTrue(max_result[0])
#
#     @weight(0)
#     def test_max_cond_var(self):
#         """autograder integration tests"""
#         # self.assertTrue(max_result[1])
#
#     @weight(0)
#     def test_max_mutex_init(self):
#         """autograder integration tests"""
#         # self.assertTrue(max_result[2])
#
#     @weight(0)
#     def test_max_thread_func(self):
#         """autograder integration tests"""
#         # self.assertTrue(max_result[3])
#
#
# if __name__ == '__main__':
#     unittest.main()
