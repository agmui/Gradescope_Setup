import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number
import json
import yaml


def run_semgrep(file_name):
    # getting semgrep for reading output
    cmd = "semgrep --quiet --config " + file_name + ".yaml ../src/" + file_name + ".c"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, encoding='UTF-8')
    result, error = process.communicate()
    print(result)

    # getting semgrep for json output
    cmd = "semgrep --quiet --config " + file_name + ".yaml ../src/" + file_name + ".c --json"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, encoding='UTF-8')
    result, error = process.communicate()
    student_output = json.loads(result)  # reading json output of semgrep

    # reading yaml file
    grader_output = ""
    with open(file_name + ".yaml", "r") as stream:
        try:
            grader_output = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print("could not read yaml")
            exit(1)

    tests_len = grader_output["rules"].__len__()
    grade_arr = [False] * tests_len
    student_index = 0
    for i in range(tests_len):
        grader_id = grader_output["rules"][i]["id"]
        student_id = student_output["results"][student_index]["check_id"]
        if grader_id == student_id:
            student_index += 1
            grade_arr[i] = True
        else:
            print("MISSING:", grader_output["rules"][i]["id"])
            print(grader_output["rules"][i])
    return grade_arr


inorder_result = run_semgrep("inorder")  # TODO: write in read me yaml file and c file must have the same name
max_result = run_semgrep("max")
# prodcons_result = run_semgrep("prodcons_condvar")


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    def test_inorder_mutex(self):
        """autograder integration tests"""
        self.assertTrue(inorder_result[0])

    @weight(0)
    def test_inorder_cond_var(self):
        """autograder integration tests"""
        self.assertTrue(inorder_result[1])

    @weight(0)
    def test_inorder_mutex_init(self):
        """autograder integration tests"""
        self.assertTrue(inorder_result[2])

    @weight(0)
    def test_inorder_thread_func(self):
        """autograder integration tests"""
        self.assertTrue(inorder_result[3])

    @weight(0)
    def test_max_mutex(self):
        """autograder integration tests"""
        self.assertTrue(max_result[0])

    @weight(0)
    def test_max_cond_var(self):
        """autograder integration tests"""
        self.assertTrue(max_result[1])

    @weight(0)
    def test_max_mutex_init(self):
        """autograder integration tests"""
        self.assertTrue(max_result[2])

    @weight(0)
    def test_max_thread_func(self):
        """autograder integration tests"""
        self.assertTrue(max_result[3])


if __name__ == '__main__':
    unittest.main()
