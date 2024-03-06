import os, sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility

sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.integrationlib import test_run

os.chdir("user")  # TODO: find out y dis here


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

        # truncated_file_arr, offset = init_ordered("arraylist.c", "struct arraylist *al_new(void)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, arraylist_decision_graph,
        #                                   arraylist_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)
        # print("errors:", inorder_errors)
        errors = test_run("arraylist.c", "struct arraylist *al_new(void)", arraylist_decision_graph,
                          arraylist_graph_convert)
        self.assertTrue(len(errors) == 0)

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

        errors = test_run("arraylist.c", "void al_free(struct arraylist *al)", al_free_decision_graph,
                          al_free_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_al_get_at(self):
        """autograder al_get_at test"""
        # ========== al_get_at ==========
        print("========== al_get_at ==========")
        al_get_at_decision_graph = {
            'head': ['root', 'alt', 'oneline', 'twoline'],
            'root': [],
            'alt': [],
            'oneline': [],
            'twoline': []
        }
        al_get_at_graph_convert = {

            'root': [
                ["if.*(pos.*>.*->size.*)", "if(.*->size.*<pos)", "if.*(pos.*>.*->capacity.*)", "if(.*->capacity<pos)"],
                ["return 0xffffffff", "return -1"],
                "return.*->list.*[pos].*"
            ],
            'alt': [
                ["if.*(pos.*<.*->size.*)", "if.*(pos.*<.*->capacity.*)"],
                ["return.*->list.*[pos];", ".*->list.*+.*"],
                ["return 0xffffffff", "return -1"]
            ],
            'oneline': [
                ["return.*pos.*0.&&.pos.<.*->size).*?.*->list[pos].*:.*0xffffffff",
                 "return.*pos.*0.&&.pos.<.*->size).*?.*0xffffffff :.*->list[pos]"]
            ],
            'twoline': [
                ["if.*(pos.*>.*->size.*).*return 0xffffffff",
                 "if(.*->size.*<pos).*return 0xffffffff",
                 "if.*(pos.*>.*->capacity.*).*return 0xffffffff",
                 "if(.*->capacity<pos).*return 0xffffffff"],
                ["return.*->list.*[pos];", ".*->list.*+.*"],
            ]
        }

        errors = test_run("arraylist.c", "int al_get_at(struct arraylist *al, int pos)",
                          al_get_at_decision_graph, al_get_at_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_al_resize(self):
        """autograder al_resize test"""
        # ========== al_resize ==========
        print("========== al_resize ==========")
        decision_graph = {
            'head': ['malloc_first', 'cap_first'],
            'malloc_first': ['memcopy', 'for_copy'],
            'cap_first': [],
            'for_copy': [],
            'memcopy': []
        }
        graph_convert = {
            'malloc_first': [
                [".*malloc(.*->capacity\*2.*)", ".*malloc(2.*->capacity.*)"],
                # "for.*(.*)",
                # [".*->list[i].*", ".*->list.*+.*i"],
                # ".*->capacity\*2;",
                # "free(.*)"
            ],
            'cap_first': [
                ".*->capacity\*.*2;",
                [".*malloc(.*->capacity.*)", ".*malloc(\*.*->capacity.*)"],
                "memcpy(.*)",
                "free(.*)"
            ],
            'for_copy': [
                "for(.*)",
                [".*->list[i].*", ".*->list.*+.*i"],
                ".*->capacity\*2;",
                "free(.*)"
            ],
            'memcopy': [
                # [".*malloc(.*->capacity\*2.*)", ".*malloc(2.*->capacity.*)"],
                "memcpy(.*)",
                ".*->capacity\*2;",
                "free(.*)"
            ]
        }

        errors = test_run("arraylist.c", "void al_resize(struct arraylist *al)",
                          decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_al_append(self):
        """autograder al_append test"""
        # ========== al_append ==========
        print("========== al_append ==========")
        decision_graph = {
            'head': ['root', 'alt'],
            'root': [],
            'alt': []
        }
        graph_convert = {
            'root': [
                ["if(.*->size.*->capacity)\nal_resize(.*)", "if(.*->size.*->capacity).*al_resize(.*)"],
                ".*->list.*->size.*=val;",
                [".*->size++.*", ".*->size.*+.*1"]
            ],
            'alt': [
                "if(.*->size.*->capacity)",
                ".*al_resize(.*)",
                ".*->list.*->size.*=val;",
                [".*->size++.*", ".*->size.*+.*1"]
            ],
        }

        errors = test_run("arraylist.c", "void al_append(struct arraylist *al, int val)", decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_sleep(self):
        """autograder sleep test"""
        # ========== sleep ==========
        print("========== sleep.c ==========")
        decision_graph = {
            'head': ['root', 'alt_if'],
            'root': [],
            'alt_if': []
        }
        graph_convert = {
            'root': [
                "if.*(argc.*)",
                "printf(.*)",
                "sleep(.*)",
                "exit(0)"
            ],
            'alt_if': [
                ["if.*(argc.*)\nprintf(.*)", "if.*(argc.*) printf(.*)"],
                "sleep(.*)",
                "exit(0)"
            ]
        }

        errors = test_run("sleep.c", "int main(int argc, char **argv)", decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)

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
                ["return\*val1.*+.*\*val2", "return\*val2.*+.*\*val1"]
            ],
        }

        errors = test_run("warmup.c", "int add_with_pointers(int *val1, int *val2)", decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_ensure_correct_order(self):
        """autograder ensure correct order test"""
        # ========== ensure correct order ==========
        print("========== ensure_correct_order ==========")
        decision_graph = {
            'head': ['root', 'flip'],
            'root': [],
            'flip': []
        }
        graph_convert = {
            'root': [
                ["if.*(\*should_be_smaller.*>.*\*should_be_larger)",
                 "if.*(\*should_be_larger.*<.*\*should_be_smaller)"],
                "int .*=\*should_be_smaller;",
                "\*should_be_smaller=\*should_be_larger;",
                "\*should_be_larger=.*;"
            ],
            'flip': [
                ["if.*(\*should_be_smaller.*>.*\*should_be_larger)",
                 "if.*(\*should_be_larger.*<.*\*should_be_smaller)"],
                "int .*=\*should_be_larger;",
                "\*should_be_larger=\*should_be_smaller;",
                "\*should_be_smaller=.*;"
            ]
        }

        errors = test_run("warmup.c", "void ensure_correct_order(int *should_be_smaller, int *should_be_larger)",
                          decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_special_equals(self):
        """autograder special_equals test"""
        # ========== special equals ==========
        print("========== special_equals ==========")
        decision_graph = {
            'head': ['elseif', 'multi', 'oneline', 'nest_oneline'],
            'elseif': [],
            'multi': [],
            'oneline': [],
            'nest_oneline': []
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
            ],
            'nest_oneline': [
                "return.*?2:(.*?1:0)"
            ]
        }

        errors = test_run("warmup.c", "int special_equals(int *val1, int *val2)", decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)

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
                "\*output=0",
                ["while(.*)", "for(.*)"],
                "if(.*)",
                "if(.*)",
            ],
            'after': [
                ["while(.*)", "for(.*)"],
                "if(.*)",
                "if(.*)",
                "\*output=0",
            ]
        }

        errors = test_run("warmup.c", "void string_with_q(char *s1, char *s2, char **output)",
                          decision_graph, graph_convert)
        self.assertTrue(len(errors) == 0)


if __name__ == '__main__':
    unittest.main()
