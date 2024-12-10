import unittest
import os
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

def editOutput(json_data):
    for test_json in json_data["tests"]:
        test_json["output_format"] = "ansi"
        # test_json["output_format"] = "md"
        # test_json["output_format"] = "html"
    with open("/autograder/hw/test_suite/src/base64gif.html") as gif:
        acc = ""
        # for line in gif:
        #     acc += line[:-1]
        json_data["tests"].insert(0, { # inserts image as base64 format
            "status": "passed",
            # "output": '<img alt="gif" src="/autograder/hw/test_suite/src/out.gif">',
            # "output": f'<img alt="gif" src="data:image/gif;base64,{acc}">',
            "output": gif.read(),
            "output_format": "html"
        })

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible',
                       stdout_visibility=True,
                       post_processor=editOutput,
                       stream=f).run(suite)
