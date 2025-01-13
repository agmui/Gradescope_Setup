import os
import sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility
sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils.integrationlib import test_run


os.chdir("kernel")  # TODO: plz remove all uses of chdir

add_to_list_decision_graph = {
    'head': ['root'],
    'root': [],
}
add_to_list_graph_convert = {
    'root': [
        "acquire(.*)",
        "list_add_tail(.*)",
        "release(.*)"
    ],
}


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @visibility('hidden')
    def test_procinit(self):
        """autograder procinit integration tests"""
        # ========== procinit ==========
        print("========== procinit ==========")
        procinit_decision_graph = {
            'head': ['lock_first', 'lock_second'],
            'lock_first': [],
            'lock_second': []
        }
        procinit_graph_convert = {
            'lock_first': [
                "initlock(.*)",
                "init_list_head(.*)",
                "for(.*).*",
                "init_list_head(.*)"
            ],
            'lock_second': [
                "init_list_head(.*)",
                "initlock(.*)",
                "for(.*).*",
                "init_list_head(.*)"
            ]
        }

        # truncated_file_arr, offset = init_ordered("proc.c", "procinit(void)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, procinit_decision_graph,
        #                                   procinit_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)

        errors = test_run("proc.c", "procinit(void)",
                          procinit_decision_graph, procinit_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_userinit(self):
        """autograder userinit integration tests"""
        # ========== userinit ==========
        print("========== userinit ==========")
        userinit_decision_graph = {
            'head': ['root'],
            'root': [],
        }
        userinit_graph_convert = {
            'root': [
                "list_add_tail(.*)"
            ],
        }

        # truncated_file_arr, offset = init_ordered("proc.c", "userinit(void)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, userinit_decision_graph,
        #                                   userinit_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)

        errors = test_run("proc.c", "userinit(void)",
                          userinit_decision_graph, userinit_graph_convert)
        self.assertTrue(len(errors) == 0)

    # TODO: add case for allocproc
    @weight(0)
    @visibility('hidden')
    def test_fork(self):
        """autograder fork integration tests"""
        # ========== fork, yield, wakeup, kill ==========
        print("========== fork ==========")
        add_to_list_decision_graph = {
            'head': ['root'],
            'root': [],
        }
        add_to_list_graph_convert = {
            'root': [
                "acquire(&runq_lock)",
                "list_add_tail(.*,.*np.*)",
                "release(&runq_lock)",
            ],
        }
        # truncated_file_arr, offset = init_ordered("proc.c", "fork(void)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, add_to_list_decision_graph,
        #                                   add_to_list_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)
        #
        errors = test_run("proc.c", "fork(void)",
                          add_to_list_decision_graph, add_to_list_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_yield(self):
        """autograder yield integration tests"""
        # ========== yield ==========
        print("========== yield ==========")
        # truncated_file_arr, offset = init_ordered("proc.c", "yield(void)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, add_to_list_decision_graph,
        #                                   add_to_list_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)
        errors = test_run("proc.c", "yield",
                          add_to_list_decision_graph, add_to_list_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_wakeup(self):
        """autograder wakeup integration tests"""
        # ========== wakeup ==========
        print("========== wakeup ==========")
        # truncated_file_arr, offset = init_ordered("proc.c", "wakeup(void *chan)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, add_to_list_decision_graph,
        #                                   add_to_list_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)
        #
        errors = test_run("proc.c", "wakeup(void *chan)",
                          add_to_list_decision_graph, add_to_list_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_kill(self):
        """autograder kill integration tests"""
        # ========== kill ==========
        print("========== kill ==========")
        #
        # truncated_file_arr, offset = init_ordered("proc.c", "kill(int pid)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, add_to_list_decision_graph,
        #                                   add_to_list_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)
        #
        errors = test_run("proc.c", "kill(int pid)",
                          add_to_list_decision_graph, add_to_list_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_scheduler(self):
        """autograder scheduler integration tests"""
        # Aidan Kirk 34,Thomas Boes,Joseph Parsons,Austin Vesich,luke
        # ========== scheduler ==========
        print("========== scheduler ==========")
        scheduler_decision_graph = {
            'head': ['wfi_before', 'wfi_after'],
            'wfi_before': ['context_switch'],
            'wfi_after': ['context_switch'],
            'context_switch': ['acquire_first', 'acquire_second', 'acquire_third'],
            'acquire_first': ['release_runq_lock'],
            'acquire_second': ['release_runq_lock'],
            'acquire_third': ['release_runq_lock'],
            'release_runq_lock': []
        }
        scheduler_graph_convert = {
            'wfi_before': [
                "acquire(.*)",
                ".*(.*==.*)",
                "release(.*)",
                "__wfi()"
            ],
            'wfi_after': [
                "acquire(.*)",
                ".*(.*\!=.*)",
            ],
            'context_switch': [
                ["(struct proc\* ?)", "(struct proc \* ?)"],
            ],
            'acquire_first': [
                "acquire(.*p.*)",
                ["list_del_init(.*)", "list_del(.*)"],
                "release(.*)",
            ],
            'acquire_second': [
                ["list_del_init(.*)", "list_del(.*)"],
                "acquire(.*p.*)",
                "release(.*)",
            ],
            'acquire_third': [
                ["list_del_init(.*)", "list_del(.*)"],
                "release(.*)",
                "acquire(.*p.*)",
            ],
            'release_runq_lock': [
                "release(.*p.*)"
            ],
            'wfi': [
                "__wfi()",
            ]
        }

        # truncated_file_arr, offset = init_ordered("proc.c", "scheduler(void)")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, scheduler_decision_graph, scheduler_graph_convert, format_arr)
        # format_output(truncated_file_arr, format_arr, offset)

        errors = test_run("proc.c", "scheduler(void)",
                          scheduler_decision_graph, scheduler_graph_convert)
        self.assertTrue(len(errors) == 0)

    @weight(0)
    @visibility('hidden')
    def test_proc_struct(self):
        """autograder proc struct integration tests"""
        # ========== proc struct ==========
        print("========== proc struct ==========")
        proc_struct_decision_graph = {
            'head': ['root'],
            'root': [],
        }
        proc_struct_graph_convert = {
            'root': [
                "struct list_head .*"
            ],
        }

        # truncated_file_arr, offset = init_ordered("proc.h", "struct proc {")
        # format_arr: list = ['n'] * len(truncated_file_arr)  # for printing output
        # errors, format_arr = graph_search('head', 0, truncated_file_arr, proc_struct_decision_graph,
        #                                   proc_struct_graph_convert,
        #                                   format_arr)
        # format_output(truncated_file_arr, format_arr, offset)
        #
        errors = test_run("proc.h", "struct proc {",
                          proc_struct_decision_graph, proc_struct_graph_convert)
        self.assertTrue(len(errors) == 0)


if __name__ == '__main__':
    unittest.main()
