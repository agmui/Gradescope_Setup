import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

def test(json_data):
    for test_json in json_data["tests"]:
        test_json["output_format"] = "ansi"
        # test_json["output_format"] = "md"
        # test_json["output_format"] = "html"

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible',
                       stdout_visibility=True,
                       post_processor=test,
                       stream=f).run(suite)
