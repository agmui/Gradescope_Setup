import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt


async def async_run_cmd(cmd):
    print("running:", cmd) #TODO: if the file is not present dont say running
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=90)
    except asyncio.TimeoutError:
        return {"code": 1,
                "output": "asyncio.TimeoutError"}

    print("finished:", cmd)
    if stdout:
        return {"code": proc.returncode,
                "output": stdout.decode()}
    if stderr:
        return {"code": proc.returncode,
                "output": stderr.decode()}

async def run():
    return await asyncio.gather(
        async_run_cmd('./band.bin'),
        async_run_cmd('./littleredhen.bin'),
        async_run_cmd('./priority.bin'),
        async_run_cmd('./threeJobs.bin'),
    )




os.chdir("src")
os.system("make")

print("===starting tests===")
inorder_output, output2, output3, output4 = asyncio.run(run())

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_band(self):
        """autograder output tests"""
        print(inorder_output['output'])
        self.assertTrue(True)

    @weight(0)
    @number("2")
    def test_little_red_hen(self):
        """autograder output tests"""
        print(output2['output'])
        self.assertTrue(True)

    @weight(0)
    @number("3")
    def test_priority(self):
        """autograder output tests"""
        print(output3['output'])
        self.assertTrue(True)

    @weight(0)
    @number("4")
    def test_three_jobs(self):
        """autograder output tests"""
        print(output4['output'])
        # process = subprocess.Popen(['../src/make grade'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        # print(result)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
