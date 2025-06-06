import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import sys
sys.path.insert(0, '../..')  # adds the hw project dir to the python path
from hw.grading_utils import random_utils

def editOutput(json_data):
    json_data["tests"][0]["output_format"] ="ansi"
    for test_json in json_data["tests"][1:]:
        # test_json["output_format"] = "ansi"
        # test_json["output_format"] = "md"
        test_json["output_format"] = "html"
    with open("/autograder/hw/test_suite/src/base64gif.txt") as gif:
        json_data["tests"].insert(1, { # inserts gif as base64 format
            "status": "passed",
            # "output": f'<img alt="gif" src="data:image/gif;base64,{gif.read()}">',
            "output": '<h1>Weekly OS memes:</h1>\n<img width="400" alt="tux" src="https://raw.githubusercontent.com/agmui/Gradescope_Setup/refs/heads/main/img/autograder_images/vim_example.jpg">',
            "output_format": "html"
        })

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible',
                       stdout_visibility=True,
                       post_processor=editOutput,
                       stream=f).run(suite)
