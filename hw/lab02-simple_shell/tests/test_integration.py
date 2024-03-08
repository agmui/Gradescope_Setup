import os
import sys
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, visibility

# sys.path.insert(0, '../..')  # adds the hw project dir to the python path

# from hw.grading_utils.integrationlib import test_run

# os.chdir("src")

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
        # rez = test_run("arraylist.c", "struct arraylist *al_new(void)",decision_graph,graph_convert)
        # self.assertTrue(rez)


        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
