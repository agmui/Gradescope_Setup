import subprocess
import re
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number


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


def ordered_pattern(pattern_arr, start_index, off_set, truncated_file_arr):
    # ========================= substring search ========================
    truncated_file_arr = truncated_file_arr[start_index:]
    format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
    past = -1
    line_num = 0
    errors = 0
    for sub_str in pattern_arr:
        if not isinstance(sub_str, list):  # to wrap substring in arr
            sub_str = [sub_str]
        for comment_index in sub_str:
            for c in ['(', ')', '+', '=']:  # formatting input for re
                comment_index = comment_index.replace(c, '\\' + c)
            arr = [line for line in truncated_file_arr if re.findall(comment_index, line)]
            if len(arr) != 0:
                line_num = truncated_file_arr.index(arr[0])
                truncated_file_arr[line_num] = ""  # delete line so it does not get used again
                break
        if line_num < past:
            format_arr[line_num] = 'w'
            errors += 1
        elif line_num == past:
            if type(format_arr[line_num]) == str:
                format_arr[line_num] = sub_str
            else:
                format_arr[line_num].append(sub_str[0])
            errors += 1
        else:
            format_arr[line_num] = 'o'

        past = line_num

    # ========================= printing output ========================
    # finding last non 'n'
    for i, c in enumerate(reversed(format_arr)):
        if c != 'n':
            last_pattern = start_index + len(format_arr) - i - 1
            break

    print_out = ""
    s = off_set + start_index
    for i, line in enumerate(file_arr[s:]):
        match format_arr[i]:
            case 'o':
                print_out += f'{bcolors.OKGREEN}{s + i + 1:4d} | {line}{bcolors.ENDC}\n'
            case 'w':
                print_out += f'{bcolors.WARNING}{s + i + 1:4d} | {line} \t\t out of order{bcolors.ENDC}\n'
            case 'n':
                print_out += f'{s + i + 1:4d} | {line}\n'
            case _:  # missing/error case
                print_out += f'{s + i + 1:4d} | {line}\n'
                print_out += f'{bcolors.FAIL} missing {format_arr[i]}{bcolors.ENDC}\n'
        if start_index + i == last_pattern:
            return errors, last_pattern, print_out

    return errors, last_pattern, print_out


"""
# reading file into arr
file = open("../src/inorder.c")
file_arr = file.read().split('\n')
file.close()

# must define bounding function area of code is in
# bounding_func = "void *thread(void *arg)"
# inorder_pattern_arr = [  # wild cards are defined by .*
#     "pthread_mutex_lock(.*)",
#     "while(.*)",
#     "pthread_cond_wait(.*)",
#     [".*++;", ".*+=.*"],
#     "pthread_mutex_unlock(.*)",
#     ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"]
# ]
# ordered_pattern(file_arr, bounding_func, inorder_pattern_arr)
"""

file = open("../src/max.c")
file_arr = file.read().split('\n')
file.close()

bounding_func = "void *thread(void *arg)"
max_pattern_arr = [
    "pthread_mutex_lock(",
    "while",
    "pthread_cond_wait(",
    "++;",
    "pthread_mutex_unlock(",
    "sleep(1)",
    "pthread_mutex_lock(",
    "--;",
    "pthread_mutex_unlock(",
    ["pthread_cond_signal(", "pthread_cond_broadcast("]
]
# ordered_pattern(file_arr, bounding_func, max_pattern_arr)

graph_convert = {
    'root': [
        "pthread_mutex_lock(.*)",
        "while(.*)",
        "pthread_cond_wait(.*)"
    ],
    'plus_rout': [
        "++;",
        "pthread_mutex_unlock(.*)",
        "sleep(1)",
        "pthread_mutex_lock(.*)",
        "--;",
    ],
    'min_rout': [
        "--;",
        "pthread_mutex_unlock(.*)",
        "sleep(1)",
        "pthread_mutex_lock(.*)",
        "++;",
    ],
    'unlock_first': [
        "pthread_mutex_unlock(.*)",
        ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"]
    ],
    'signal_first': [
        ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"],
        "pthread_mutex_unlock(.*)",
    ],
}
decision_graph = {
    'head': ['root'],
    'root': ['plus_rout', 'min_rout'],
                  'plus_rout': ['unlock_first', 'signal_first'],
                  'min_rout': ['unlock_first', 'signal_first'],
                  'unlock_first': [],
                  'signal_first': [],
                  }

# use greedy DFS to search graph

def init_ordered(file_arr, bounding_func):
    # ====================  getting function scope ====================
    off_set = -1
    end_index: int = 0
    cur_count = 0
    for i, line in enumerate(file_arr):
        if bounding_func in line:
            off_set = i
        if off_set != -1:
            if '{' in line:
                cur_count += 1
            if '}' in line:
                cur_count -= 1
            if cur_count == 0 and off_set != i:
                end_index = i
                break

        # removing comments from file_arr
        comment_index = line.find("//")
        if comment_index != -1:
            file_arr[i] = line[:comment_index]

    # truncate file_arr to only the function scope
    return file_arr[off_set:end_index + 1], off_set


truncated_file_arr, off_set = init_ordered(file_arr, bounding_func)


def graph_search(node, off_set, start_index):
    num_of_s = len(decision_graph[node])
    num_of_err = [0] * num_of_s
    print_outs = [""] * num_of_s
    start_index_cp = start_index
    for i, successor in enumerate(decision_graph[node]):
        num_of_err[i], start_index, print_outs[i] = ordered_pattern(graph_convert[successor], start_index_cp + 1,
                                                                    off_set, truncated_file_arr)
        if num_of_err[i] == 0:
            print(print_outs[0], end='')
            graph_search(successor, off_set, start_index)
            return
    if num_of_s == 0:
        return
    successor_index = num_of_err.index(min(num_of_err))
    print(print_outs[successor_index], end='')
    graph_search(decision_graph[node][successor_index], off_set, start_index)


# err, start_index, print_out = ordered_pattern(graph_convert['root'], 0, off_set, truncated_file_arr)
# print(print_out, end='')
# graph_search('root', off_set, start_index)
graph_search('head', off_set-1, 0)

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
