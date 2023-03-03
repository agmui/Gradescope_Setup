import subprocess
import re
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number


# TODO: remove white space in file before scan
# TODO: pattern leaking into another node

# for colored output
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


def init_ordered(file_location: str, bounding_func: str) -> [list, int]:
    """
    Preps file to be run in ordered_pattern().
    Finds the bounds of the function in the file

    :param file_location: file that is to be parsed
    :param bounding_func: the function that is to be scanned
    :return: array containing only the function's code, offset to the function from the top of the file
    """
    # ====================  getting function scope ====================
    file = open(file_location)
    file_arr = file.read().split('\n')
    file.close()

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

        # removing comments from code_arr
        comment_index = line.find("//")
        if comment_index != -1:
            file_arr[i] = line[:comment_index]

    # truncate code_arr to only the function scope
    return file_arr[off_set:end_index + 1], off_set


# NOTE: The formatted output is printed in sections because the function jumps from node to node.
# So everytime it jumps is just resumes from where the last node left off. That is why there is
# an inner_func_offset argument
def graph_search(cur_node: str, func_offset: int, inner_func_offset: int, file_arr: list[str],
                 decision_graph: dict, graph_to_pattern: dict):
    """
    Greedy DFS graph search for the least number of errors.

    NOTE: once it has reached the end of the graph it does not go back and check the other nodes

    :param cur_node: the current node that is being scanned
    :param func_offset: offset from the top of the page to the function
    :param inner_func_offset: offset from the top of the function to the line focused on
    :param file_arr: The parsed file array that is being scanned
    :param decision_graph: graph that is searched on
    :param graph_to_pattern: translation between nodes in the graph to the patterned array
    """
    num_of_s = len(decision_graph[cur_node])  # number of successors of the current node
    if num_of_s == 0:  # terminating case
        return {}
    dict_of_err = [{}] * num_of_s  # array of the results of the errors
    num_of_err = [0] * num_of_s  # array of the number of errors each successor returns
    print_outs = [""] * num_of_s  # array of formatted output each successor returns
    # cp of the inner_func_offset, so it does not get overwritten when running through the successors
    start_index = inner_func_offset + 1
    # print("route:", cur_node)
    for i, successor in enumerate(decision_graph[cur_node]):
        # ===
        # print("trying:", successor)
        # if successor == "unlock_first":
        #     pass
        # ===
        dict_of_err[i], inner_func_offset, print_outs[i] = ordered_pattern(graph_to_pattern[successor],
                                                                           func_offset + start_index,
                                                                           file_arr[start_index:])
        inner_func_offset += start_index
        if len(dict_of_err[i]) == 0:  # if 0 errors are found just print result immediately
            print(print_outs[i], end='')
            ret_dict = graph_search(successor, func_offset, inner_func_offset, file_arr, decision_graph,
                                    graph_to_pattern)
            return dict_of_err[i] | ret_dict
        num_of_err[i] = len(dict_of_err)
    successor_index = num_of_err.index(min(num_of_err))  # finding which successor had the lease number of errors
    print(print_outs[successor_index], end='')  # printing formatted output
    ret_dict = graph_search(decision_graph[cur_node][successor_index], func_offset, inner_func_offset, file_arr,
                            decision_graph, graph_to_pattern)
    return dict_of_err[successor_index] | ret_dict


def ordered_pattern(pattern_arr: list, total_offset: int, truncated_arr: list) -> [dict, int, str]:
    """
    Searches for a pattern in the truncated array.
    Total offset is so the formatted output has the correct line numbers relative to the original file.

    :param pattern_arr: the pattern list that is to be searched
    :param total_offset: total offset from the top of the file
    :param truncated_arr: the portion of the file that will be searched
    :return: dict of errors, last pattern line number it stopped at, formatted output for terminal
    """
    # ========================= substring search ========================
    code_arr = truncated_arr.copy()
    format_arr: list = ['n'] * len(code_arr)  # for printing output
    past = -1
    line_num = 0
    errors = {}
    for sub_str in pattern_arr:
        if not isinstance(sub_str, list):  # to wrap substring in arr
            sub_str = [sub_str]
        for comment_index in sub_str:
            for c in ['(', ')', '+', '=']:  # formatting input for re
                comment_index = comment_index.replace(c, '\\' + c)
            arr = [line for line in code_arr if re.findall(comment_index, line)]
            if len(arr) != 0:
                line_num = code_arr.index(arr[0])
                code_arr[line_num] = ""  # delete line so it does not get used again
                break
        error_str = ""
        if line_num < past:
            format_arr[line_num] = 'w'
            error_str = "out of order line: " + str(line_num)
        elif line_num == past or (past == -1 and line_num == 0):
            if type(format_arr[line_num]) == str:
                format_arr[line_num] = sub_str
            else:
                format_arr[line_num].append(sub_str[0])
            error_str = "missing line: " + str(line_num)
        else:
            format_arr[line_num] = 'o'

        # error formating
        if error_str:
            if sub_str[0] not in errors:
                errors[sub_str[0]] = [error_str]
            else:
                errors[sub_str[0]].append(error_str)

        past = line_num

    # ========================= formatting output ========================
    # finding last searched pattern
    last_pattern = 0
    for i, c in enumerate(reversed(format_arr)):
        if c != 'n':
            last_pattern = len(format_arr) - i - 1
            break

    print_out = ""
    for i, line in enumerate(truncated_arr):
        match format_arr[i]:
            case 'o':
                print_out += f'{bcolors.OKGREEN}{total_offset + i + 1:4d} | {line}{bcolors.ENDC}\n'
            case 'w':
                print_out += f'{bcolors.WARNING}{total_offset + i + 1:4d} | {line} \t\t out of order{bcolors.ENDC}\n'
            case 'n':
                print_out += f'{total_offset + i + 1:4d} | {line}\n'
            case _:  # missing/error case
                print_out += f'{total_offset + i + 1:4d} | {line}\n'
                print_out += f'{bcolors.FAIL} missing {format_arr[i]}{bcolors.ENDC}\n'
        if i == last_pattern:
            return errors, last_pattern, print_out

    return errors, last_pattern, print_out


# ========== inorder ==========
print("========== inorder.c ==========")
inorder_decision_graph = {
    'head': ['root'],
    'root': ['unlock_first', 'signal_first'],
    'unlock_first': [],
    'signal_first': [],
}
inorder_graph_convert = {
    'root': [
        "pthread_mutex_lock(.*)",
        "while(.*)",
        "pthread_cond_wait(.*)",
        ["++;", "+="],
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

# truncated_file_arr, offset = init_ordered("../src/inorder.c", "void *thread(void *arg)")
# errors = graph_search('head', offset, 0, truncated_file_arr, inorder_decision_graph, inorder_graph_convert)
# print("errors:", errors)

# ========== max ==========
print("========== max.c ==========")
max_decision_graph = {
    'head': ['root'],
    'root': ['plus_rout', 'min_rout'],
    'plus_rout': ['unlock_first', 'signal_first'],
    'min_rout': ['unlock_first', 'signal_first'],
    'unlock_first': [],
    'signal_first': [],
}
max_graph_convert = {
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

truncated_file_arr, offset = init_ordered("../src/max.c", "void *thread(void *arg)")
errors = graph_search('head', offset, 0, truncated_file_arr, max_decision_graph, max_graph_convert)
print("errors:", errors)

# ========== prodcons ==========
"""
print("========== prodcons.c ==========")
# prodcons_prod_decision_graph = {
#     'head': ['root'],
#     'root': ['plus_rout', 'min_rout'],
#     'plus_rout': ['unlock_first', 'signal_first'],
#     'min_rout': ['unlock_first', 'signal_first'],
#     'unlock_first': [],
#     'signal_first': [],
# }
# prodcons_prod_graph_convert = {
#     'root': [
#         "pthread_mutex_lock(.*)",
#         "while(.*)",
#         "pthread_cond_wait(.*)"
#     ],
#     'plus_rout': [
#         "++;",
#         "pthread_mutex_unlock(.*)",
#         "sleep(1)",
#         "pthread_mutex_lock(.*)",
#         "--;",
#     ],
#     'min_rout': [
#         "--;",
#         "pthread_mutex_unlock(.*)",
#         "sleep(1)",
#         "pthread_mutex_lock(.*)",
#         "++;",
#     ],
#     'unlock_first': [
#         "pthread_mutex_unlock(.*)",
#         ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"]
#     ],
#     'signal_first': [
#         ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"],
#         "pthread_mutex_unlock(.*)",
#     ],
# }

truncated_file_arr, offset = init_ordered("../src/prodcons_condvar.c", "void *producer(void *arg)")
graph_search('head', offset, 0, truncated_file_arr, prodcons_prod_decision_graph, prodcons_prod_graph_convert)

# prodcons_cons_decision_graph = {
#     'head': ['root'],
#     'root': ['plus_rout', 'min_rout'],
#     'plus_rout': ['unlock_first', 'signal_first'],
#     'min_rout': ['unlock_first', 'signal_first'],
#     'unlock_first': [],
#     'signal_first': [],
# }
# prodcons_cons_graph_convert = {
#     'root': [
#         "pthread_mutex_lock(.*)",
#         "while(.*)",
#         "pthread_cond_wait(.*)"
#     ],
#     'plus_rout': [
#         "++;",
#         "pthread_mutex_unlock(.*)",
#         "sleep(1)",
#         "pthread_mutex_lock(.*)",
#         "--;",
#     ],
#     'min_rout': [
#         "--;",
#         "pthread_mutex_unlock(.*)",
#         "sleep(1)",
#         "pthread_mutex_lock(.*)",
#         "++;",
#     ],
#     'unlock_first': [
#         "pthread_mutex_unlock(.*)",
#         ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"]
#     ],
#     'signal_first': [
#         ["pthread_cond_signal(.*)", "pthread_cond_broadcast(.*)"],
#         "pthread_mutex_unlock(.*)",
#     ],
# }
truncated_file_arr, offset = init_ordered("../src/prodcons_condvar.c", "void *consumer(void *arg)")
graph_search('head', offset, 0, truncated_file_arr, prodcons_cons_decision_graph, prodcons_cons_graph_convert)
"""
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
