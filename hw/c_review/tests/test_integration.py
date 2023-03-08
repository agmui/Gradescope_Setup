import subprocess
import re, os
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility


# TODO: (minify) remove white space in file before scan
# TODO: make scan go down then up from offset
# TODO: when scanning there is a bug that if there is a shared pattern in two different sections and one section and the
# TODO: if there is a missing the above line does not go green/ warning
# TODO: do multi line or replacement
# top section does not contain the pattern the bottem pattern gets taken up so by consequence there is a "out of order"
# error in the first section and a missing error in the second section

# for colored output
class bcolors:
    # HEADER = ''
    # OKBLUE = ''
    # OKCYAN = ''
    # OKGREEN = ''
    # WARNING = ''
    # FAIL =''
    # ENDC =''
    # BOLD =''
    # UNDERLINE = ''

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
            format_arr[line_num] = 'w'
            error_str = "out of order line: " + str(line_num)
        elif missing:
            if type(format_arr[line_num]) == str:
                format_arr[line_num] = sub_str
            else:
                format_arr[line_num].append(sub_str[0])
            error_str = "missing line: " + str(line_num)
        else:
            format_arr[line_num] = 'o'

        # error formatting
        if error_str:
            if sub_str[0] not in errors_dict:
                errors_dict[sub_str[0]] = [error_str]
            else:
                errors_dict[sub_str[0]].append(error_str)

        past = line_num

    # finding last searched pattern
    last_pattern = 0
    for i, c in enumerate(reversed(format_arr)):
        if c != 'n':
            last_pattern = len(format_arr) - i - 1
            break

    return errors_dict, last_pattern, code_arr, format_arr


def format_output(file_arr, format_arr, total_offset):
    for i, line in enumerate(file_arr):
        match format_arr[i]:
            case 'o':
                print(f'{bcolors.OKGREEN}\tok  {total_offset + i + 1:4d} | {line}{bcolors.ENDC}\n', end='')
            case 'w':
                print(f'{bcolors.WARNING}out of order{total_offset + i + 1:4d} | {line} {bcolors.ENDC}\n', end='')
            case 'n':
                print(f'\t    {total_offset + i + 1:4d} | {line}\n', end='')
            case _:  # missing/error case
                print(f'\t    {total_offset + i + 1:4d} | {line}\n', end='')
                print(f'{bcolors.FAIL}\t missing {format_arr[i]}{bcolors.ENDC}\n', end='')


os.chdir("user")
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @visibility('hidden')
    def test_arraylist(self):
        """autograder arraylist test"""
        # ========== arraylist ==========
        print("========== arraylist.c ==========")
        arraylist_decision_graph = {
            'head': ['root'],
            'root': []
        }
        arraylist_graph_convert = {
            'root': [
                ".*malloc(sizeof(struct arraylist))",
                ["->size = 0", "->capacity = DEF_ARRAY_LIST_CAPACITY", "->list = .*malloc(.*)", "return .*"],
            ],
        }

        truncated_file_arr, offset = init_ordered("arraylist.c", "struct arraylist *al_new(void)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, arraylist_decision_graph, arraylist_graph_convert,
                                                format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_al_free(self):
        """autograder al_free test"""
        # ========== al_free ==========
        print("========== al_free ==========")
        al_free_decision_graph = {
            'head': ['root'],
            'root': []
        }
        al_free_graph_convert = {
            'root': [
                "free(.*->list)",
                "free(.*);",
            ],
        }

        truncated_file_arr, offset = init_ordered("arraylist.c", "void al_free(struct arraylist *al)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, al_free_decision_graph, al_free_graph_convert,
                                                format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_al_get_at(self):
        """autograder al_get_at test"""
        # ========== al_get_at ==========
        print("========== al_get_at ==========")
        al_get_at_decision_graph = {
            'head': ['root', 'alt', 'oneline'],
            'root': [],
            'alt': [],
            'oneline': []
        }
        al_get_at_graph_convert = {
            'root': [
                ["if.*(pos.*>.*->size.*)","if.*(pos.*>.*->capacity.*)"]
                ["return 0xffffffff","return -1"]
                "return .*->list[pos];"
            ],
            'alt': [
                ["if.*(pos.*<.*->size.*)","if.*(pos.*<.*->capacity.*)"]
                "return .*->list.*[pos];",
                ["return 0xffffffff","return -1"]
            ],
            'oneline': [
                ["return.*pos.*0.&&.pos.<.*->size).*?.*->list[pos].*:.*0xffffffff",
                "return.*pos.*0.&&.pos.<.*->size).*?.*0xffffffff :.*->list[pos]"]
            ]
        }

        truncated_file_arr, offset = init_ordered("arraylist.c", "int al_get_at(struct arraylist *al, int pos)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, al_get_at_decision_graph, al_get_at_graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_al_resize(self):
        """autograder al_resize test"""
        # ========== al_resize ==========
        print("========== al_resize ==========")
        decision_graph = {
            'head': ['malloc_first','cap_first'],
            'malloc_first': [],
            'cap_first': [],
        }
        graph_convert = {
            'malloc_first': [
                [".*malloc(.*->capacity\*2.*)",".*malloc(2.*->capacity.*)"],
                # ".*->capacity\*2;",
                "for.*(.*)",
                [".*->list[i].*",".*->list+i"],
                "free(.*)"
            ],
            'cap_first': [
                ".*->capacity\*2;",
                ".*malloc(.*->capacity\*2.*)",
                "for(.*)",
                ".*->list[i].*",
                "free(.*)"
            ],
        }

        truncated_file_arr, offset = init_ordered("arraylist.c", "void al_resize(struct arraylist *al)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_al_append(self):
        """autograder al_append test"""
        # ========== al_append ==========
        print("========== al_append ==========")
        decision_graph = {
            'head': ['root'],
            'root': []
        }
        graph_convert = {
            'root': [
                "if(.*->size.*->capacity)",
                "al_resize(.*)",
                ".*->list.*->size.*= val",
                [".*->size++",".*->size.*+.*1"]
            ],
        }

        truncated_file_arr, offset = init_ordered("arraylist.c", "void al_append(struct arraylist *al, int val)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_sleep(self):
        """autograder sleep test"""
        # ========== sleep ==========
        print("========== sleep.c ==========")
        decision_graph = {
            'head': ['root'],
            'root': []
        }
        graph_convert = {
            'root': [
                "if.*(argc.*)",
                "printf(.*)",
                "sleep(.*)",
                "exit(0)"
            ],
        }

        truncated_file_arr, offset = init_ordered("sleep.c", "int main(int argc, char **argv)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_warmup(self):
        """autograder warmup test"""
        # ========== warmup ==========
        print("========== warmup.c ==========")
        decision_graph = {
            'head': ['root'],
            'root': []
        }
        graph_convert = {
            'root': [
                ["return \*val1.*+.*\*val2", "return \*val2.*+.*\*val1"]
            ],
        }

        truncated_file_arr, offset = init_ordered("warmup.c", "int add_with_pointers(int *val1, int *val2)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)
    
    @weight(0)
    @visibility('hidden')
    def test_ensure_correct_order(self):
        """autograder ensure correct order test"""
        # ========== ensure correct order ==========
        print("========== ensure_correct_order ==========")
        decision_graph = {
            'head': ['root'],
            'root': []
        }
        graph_convert = {
            'root': [
                ["if.*(\*should_be_smaller.*>.*\*should_be_larger)", "if.*(\*should_be_larger.*<.*\*should_be_smaller)"],
                "int .* = \*should_be_smaller;",
                "\*should_be_smaller = \*should_be_larger;",
                "\*should_be_larger = .*;"
            ],
        }

        truncated_file_arr, offset = init_ordered("warmup.c", "void ensure_correct_order(int *should_be_smaller, int *should_be_larger)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)
        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_special_equals(self):
        """autograder special_equals test"""
        # ========== special equals ==========
        print("========== special_equals ==========")
        decision_graph = {
            'head': ['elseif','multi', 'oneline'],
            'elseif': [],
            'multi': [],
            'oneline': []
        }
        graph_convert = {
            'elseif': [
                "if.*(.*)",
                "return 2",
                "if.*(.*)",
                "return 1",
                "return 0",
            ],
            'multi': [
                "if.*(.*)",
                "if.*(.*)",
                "return 2",
                "return 1",
                "return 0",
            ],
            'oneline': [
                "if.*(.*).*return .*",
                "if.*(.*).*return .*",
                "return 0"
            ]
        }

        truncated_file_arr, offset = init_ordered("warmup.c", "int special_equals(int *val1, int *val2)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)

        self.assertTrue(len(errors)==0)

    @weight(0)
    @visibility('hidden')
    def test_string_with_q(self):
        """autograder string_with_q test"""
        # ========== string with q ==========
        print("========== string_with_q ==========")
        decision_graph = {
            'head': ['before', 'after'],
            'before': [],
            'after': []
        }
        graph_convert = {
            'before': [
                "\*output = 0",
                ["while(.*)", "for(.*)"],
                "if.*(.*)",
                "if.*(.*)",
            ],
            'after': [
                ["while(.*)", "for(.*)"],
                "if.*(.*)",
                "if.*(.*)",
                "\*output = 0",
            ]
        }

        truncated_file_arr, offset = init_ordered("warmup.c", "void string_with_q(char *s1, char *s2, char **output)")
        format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        errors, format_arr = graph_search('head', 0, truncated_file_arr, decision_graph, graph_convert, format_arr)
        format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)
        self.assertTrue(len(errors)==0)


if __name__ == '__main__':
    unittest.main()
