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
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
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
        async_run_cmd('./inorder'),
        async_run_cmd('./max'),
        async_run_cmd('./prodcons_condvar')
    )
    # output = [0, 0, 0]
    # task1 = asyncio.create_task(async_run_cmd('./inorder'))
    # task2 = asyncio.create_task(async_run_cmd('./max'))
    # task3 = asyncio.create_task(async_run_cmd('./prodcons_condvar'))
    # output[0] = await asyncio.wait_for(task1, timeout=15)
    # output[1] = await asyncio.wait_for(task2, timeout=15)
    # output[2] = await asyncio.wait_for(task3, timeout=15)
    # return output

os.chdir('./src')
os.system("make clean")
os.system("make")

os.chdir("../src/")
print(text2art("cond vars basic", "rand"))
class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    # @partial_credit(10.0)
    def test_us1tests(self):
        """autograder us1tests.c tests"""
        process = subprocess.Popen(
            ['./us1tests'], stdout=subprocess.PIPE, encoding='UTF-8')
        result, error = process.communicate()
        print("==========test1=========")
        print(result)
        self.assertTrue("OK" in result)

    # def test_inorder_output(output):
    #     ordered_output = [
    #         "1 is finished with the critical section",
    #         "2 is finished with the critical section",
    #         "3 is finished with the critical section",
    #         "4 is finished with the critical section"
    #     ]
    #     print("======output checking=======")
    #     if output["code"] != 0:
    #         print("exited with", output["code"])
    #         return False
    #     output = output["output"].split('\n')
    #     count: int = 0
    #     for out in output:
    #         if ordered_output[count] in out:
    #             count += 1
    #             print(out)
    #             if count == 4:
    #                 break
    #     if count != 4:
    #         print("error output not correct:", count)
    #     else:
    #         print("\noutput correct!")

    # def test_max_output(output):
    #     # output = os.system("./max")
    #     print("======output checking=======")
    #     output = output["output"].split('\n')
    #     count = 0
    #     change: bool = False
    #     for i in output:
    #         if "is in the critical section" in i:
    #             print(i)
    #             count += 1
    #             change = True
    #         elif "has left the critical section" in i:
    #             print(i)
    #             count -= 1
    #             change = True
    #         if count > 3:
    #             print("error count:", count)
    #     if count != 0:
    #         print("error output not correct:", count)
    #     if not change:
    #         print("count not read output change:", change)
    #     else:  # FIXME:
    #         print("\noutput correct!")

    # def output_prodcons_output(output):
    #     print("======output checking=======")
    #     output = output["output"].split('\n')
    #     count = 0
    #     for i in output:
    #         if "Produced value" in i:
    #             print(i, "error: producer not waiting" if count > 5 else "")
    #             count += 1
    #         elif "Consumed value" in i:
    #             print(i, "error: consumer not waiting" if count < 0 else "")
    #             count -= 1
    #     if count != 0:
    #         print("error output not correct:", count)
    #     else:
    #         print("\noutput correct!")


if __name__ == '__main__':
    unittest.main()
