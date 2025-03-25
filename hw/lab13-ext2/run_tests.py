import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

def editOutput(json_data):
    for test_json in json_data["tests"]:
        test_json["output_format"] = "ansi"
        # test_json["output_format"] = "md"
        # test_json["output_format"] = "html"
    json_data["tests"].insert(0, { # inserts image as base64 format
        "status": "passed",
        # "output": '<img alt="tux" src="/autograder/hw/grading_utils/Tux.svg.png">',
        "output": '<h1>Weekly OS memes:</h1>\n<img width="400" alt="tux" src="https://raw.githubusercontent.com/agmui/Gradescope_Setup/refs/heads/main/img/autograder_images/ext_example.png">',
        "output_format": "html"
    })

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible',
                       stdout_visibility=True,
                       post_processor=editOutput,
                       stream=f).run(suite)
