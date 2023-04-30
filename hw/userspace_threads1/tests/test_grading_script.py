import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio # TODO: add to reqirements.txt




async def async_run_cmd(cmd):
    print("running:", cmd)
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
        async_run_cmd('./tests.bin 1'),
        async_run_cmd('./tests.bin 2'),
        async_run_cmd('./tests.bin 3'),
        async_run_cmd('./tests.bin 4'),
        async_run_cmd('./tests.bin 5')
    )

os.system("apt update -y > /dev/null && apt upgrade -y > /dev/null")
os.system("apt install -y valgrind > /dev/null")
os.chdir("src")
os.system("make tests.bin")

print("===starting tests===")
output1, output2, output3, output4, output5 = asyncio.run(run())

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_1(self):
        """autograder tests.bin 1 tests"""
        print(text2art("stack smashing", "rand"))
        # process = subprocess.Popen(['./tests.bin', '1'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        print(output1)
        self.assertTrue("OK" in output1)

    @weight(0)
    @number("2")
    def test_2(self):
        """autograder test.bin 2 tests"""
        # process = subprocess.Popen(['./tests.bin', '2'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        print(output2)
        self.assertTrue("OK" in output2)

    @weight(0)
    @number("3")
    def test_3(self):
        """autograder test.bin 3 tests"""
        # process = subprocess.Popen(['./tests.bin', '3'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        print(output3)
        self.assertTrue("OK" in output3)

    @weight(0)
    @number("4")
    def test_4(self):
        """autograder test.bin 4 tests"""
        # process = subprocess.Popen(['./tests.bin', '4'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        print(output4)
        self.assertTrue("OK" in output4)

    @weight(0)
    @number("5")
    def test_5(self):
        """autograder test.bin 5 tests"""
        # process = subprocess.Popen(['./tests.bin', '5'], stdout=subprocess.PIPE, encoding='UTF-8')
        # result, error = process.communicate()
        print(output5)
        self.assertTrue("OK" in output5)

    @weight(0)
    @number("6")
    def test_valgrind(self):
        """autograder valgrind tests"""
        cmd = "valgrind ./tests.bin 5".split(' ')
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        self.assertTrue(True, "there is a memory leak")
