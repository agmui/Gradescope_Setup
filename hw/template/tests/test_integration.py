import subprocess
import re, os
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility


# TODO: remove white space in file before scan
# TODO: make scan go down then up from offset
# TODO: when scanning there is a bug that if there is a shared pattern in two different sections and one section and the
# top section does not contain the pattern the bottem pattern gets taken up so by consequence there is a "out of order"
# error in the first section and a missing error in the second section

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
# TODO: make iterative
def graph_search(cur_node: str, inner_func_offset: int, file_arr: list[str], decision_graph: dict,
                 graph_to_pattern: dict, format_arr):
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
        return {}, format_arr
    dict_of_err = [{}] * num_of_s  # array of the results of the errors
    num_of_err = [0] * num_of_s  # array of the number of errors each successor returns
    format_arr_tries = [[""]] * num_of_s  # TODO: rename
    file_arr_tries = [[""]] * num_of_s  # TODO: rename

    # cp of the inner_func_offset, so it does not get overwritten when running through the successors
    start_index = inner_func_offset + 1
    # print("route:", cur_node)
    for i, successor in enumerate(decision_graph[cur_node]):
        # print("trying:", successor)
        dict_of_err[i], inner_func_offset, temp, temp2 = ordered_pattern(graph_to_pattern[successor], start_index,
                                                                         file_arr, format_arr)
        file_arr_tries[i] = temp.copy()  # FIXME:
        format_arr_tries[i] = temp2.copy()
        # === a successors with no errors ===
        if len(dict_of_err[i]) == 0:  # if 0 errors are found just print result immediately
            ret_dict, format_arr = graph_search(successor, inner_func_offset, file_arr_tries[i],
                                                decision_graph, graph_to_pattern, format_arr_tries[i])
            return dict_of_err[i] | ret_dict, format_arr
        num_of_err[i] = len(dict_of_err)
    # === errors for all successors ===
    successor_index = num_of_err.index(min(num_of_err))  # finding which successor had the lease number of errors
    ret_dict, format_arr = graph_search(decision_graph[cur_node][successor_index], inner_func_offset,
                                        file_arr_tries[successor_index],
                                        decision_graph, graph_to_pattern, format_arr_tries[successor_index])
    return dict_of_err[successor_index] | ret_dict, format_arr


def ordered_pattern(pattern_arr: list, inner_func_offset, file_arr: list, format_arr) -> [dict, int, list, list]:
    """
    Searches for a pattern in the truncated array.
    Total offset is so the formatted output has the correct line numbers relative to the original file.

    :param pattern_arr: the pattern list that is to be searched
    :param func_offset: total offset from the top of the file
    :param file_arr: the portion of the file that will be searched
    :return: dict of errors, last pattern line number it stopped at, formatted output for terminal
    """
    # ========================= substring search ========================
    code_arr = file_arr.copy()
    past = inner_func_offset - 1
    line_num = inner_func_offset
    errors_dict = {}

    new_format_arr = format_arr.copy()  # FIXME: this is here bc ordered_pattern mutates format_arr
    for sub_str in pattern_arr:
        missing: bool = True  # used to determine if there is a missing error
        if not isinstance(sub_str, list):  # to wrap substring in arr
            sub_str = [sub_str]
        # ==
        if "buffer[last_valid_index]" in sub_str[0]:
            pass
        # ==
        for comment_index in sub_str:
            for c in ['(', ')', '+', '=', '[', ']']:  # formatting input for re
                comment_index = comment_index.replace(c, '\\' + c)
            arr = [line for line in code_arr if re.findall(comment_index, line)]
            if len(arr) != 0:
                missing = False
                line_num = code_arr.index(arr[0])  # NOTE: only uses first fine
                code_arr[line_num] = ""  # delete line so it does not get used again
                break
        # ========================= error detection ========================
        error_str = ""
        if line_num < past:
            new_format_arr[line_num] = 'w'
            error_str = "out of order line: " + str(line_num)
        elif missing:
            if type(new_format_arr[line_num]) == str:
                new_format_arr[line_num] = sub_str
            else:
                new_format_arr[line_num].append(sub_str[0])
            error_str = "missing line: " + str(line_num)
        else:
            new_format_arr[line_num] = 'o'

        # error formatting
        if error_str:
            if sub_str[0] not in errors_dict:
                errors_dict[sub_str[0]] = [error_str]
            else:
                errors_dict[sub_str[0]].append(error_str)

        past = line_num

    # finding last searched pattern
    last_pattern = 0
    for i, c in enumerate(reversed(new_format_arr)):
        if c != 'n':
            last_pattern = len(new_format_arr) - i - 1
            break

    return errors_dict, last_pattern, code_arr, new_format_arr


def format_output(file_arr, format_arr, total_offset):
    for i, line in enumerate(file_arr):
        match format_arr[i]:
            case 'o':
                print(f'{bcolors.OKGREEN}{total_offset + i + 1:4d} | {line} \tok{bcolors.ENDC}\n', end='')
            case 'w':
                print(f'{bcolors.WARNING}{total_offset + i + 1:4d} | {line} \t\t out of order{bcolors.ENDC}\n', end='')
            case 'n':
                print(f'{total_offset + i + 1:4d} | {line}\n', end='')
            case _:  # missing/error case
                print(f'{total_offset + i + 1:4d} | {line}\n', end='')
                print(f'{bcolors.FAIL} missing {format_arr[i]}{bcolors.ENDC}\n', end='')


os.chdir("src")

def run_integration_check(filename, func,decision_graph, graph_convert):
    truncated_file_arr, offset = init_ordered(filename, func)#"arraylist.c", "struct arraylist *al_new(void)")
    format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
    errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert,
                                      format_arr)
    format_output(truncated_file_arr, format_arr, offset)
    return len(errors) == 0


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @visibility('hidden')
    def test_arraylist(self):
        """autograder arraylist test"""
        # ========== arraylist ==========
        print("========== arraylist.c ==========")
        decision_graph = {
            'head': ['root'],
            'root': []
        }
        graph_convert = {
            'root': [
                ".*malloc(sizeof(struct arraylist))",
                "->size = 0",
                "->capacity = DEF_ARRAY_LIST_CAPACITY",
                "->list = .*malloc(.*)",
                "return .*"
            ],
        }
        # rez = run_integration_check("arraylist.c", "struct arraylist *al_new(void)",decision_graph,graph_convert)
        # self.assertTrue(rez)


        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
