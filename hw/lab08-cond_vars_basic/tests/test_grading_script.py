import os
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit
from art import *
import asyncio  # TODO: add to reqirements.txt
import re


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
        async_run_cmd('./inorder.bin'),
        async_run_cmd('./max.bin'),
        # async_run_cmd('./prodcons_condvar'),
        async_run_cmd('./rooms.bin'),
        async_run_cmd('./tunnel.bin')
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
# os.system("make clean")
# os.system("make")

print("===starting tests===")
inorder_output, max_output, rooms_output, tunnel_output = asyncio.run(run())


# print("====================")
# print("inorder")
# print("====================")
# inorder_result = inorder_tests(output[0])
# print()
# print("====================")
# print("max")
# print("====================")
# max_result = max_tests(output[1])
# print()
# print("====================")
# print("prodcons")
# print("====================")
# prodcons_result = prodcons_tests(output[2])
# print(inorder_result, max_result, prodcons_result)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    def test_inorder_output(self):
        print(text2art("cond vars basic", "rand"))
        global inorder_output
        ordered_output = [
            "1 is finished with the critical section",
            "2 is finished with the critical section",
            "3 is finished with the critical section",
            "4 is finished with the critical section"
        ]
        print("======output checking=======")
        if inorder_output["code"] != 0:
            print("exited with", inorder_output["code"])
            self.assertTrue(False)
        inorder_output = inorder_output["output"].split('\n')
        count: int = 0
        for out in inorder_output:
            if ordered_output[count] in out:
                count += 1
                print('\t' + out)
                if count == 4:
                    break
            else:
                print(out)
        if count != 4:
            print("error output1 not correct:", count)
            self.assertTrue(False)
        else:
            print("\noutput correct!")
            self.assertTrue(True)

    def test_max_output(self):
        print("======output checking=======")
        output = max_output["output"].split('\n')
        count = 0
        change: bool = False
        exceeded_count = False
        for i in output:
            if "is in the critical section" in i:
                print('\t' + i)
                count += 1
                change = True
            elif "has left the critical section" in i:
                print('\t' + i)
                count -= 1
                change = True
            else:
                print(i)
            if count > 3:
                print("== error count:", count, '==')
                exceeded_count = True
        if count != 0:
            print("error output not correct:", count)
            self.assertTrue(False)
        if not change:
            print("count not read output change:", change)
            self.assertTrue(False)
        if exceeded_count:
            print("error: exceeded count")
            self.assertTrue(False)
        else:  # FIXME:
            print("\noutput correct!")
            self.assertTrue(True)

    # def test_prodcons_output(self):
    #     print("======output checking=======")
    #     output = output3["output"].split('\n')
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
    #         self.assertTrue(False)
    #     else:
    #         print("\noutput correct!")
    #         self.assertTrue(True)

    def test_rooms_output(self):
        print("======output checking=======")
        output = rooms_output["output"].split('\n')
        if len(output) <= 0:
            print("no output!!?!")
            self.assertTrue(False)
            return

        error = False
        room1 = 0
        waiting_room2 = 0
        room2 = 0
        unhappy = 0
        final_number = 0
        for i in output[:-1]:
            print(i)
            if "Just arrived" in i:
                continue
            elif "Entered first room" in i:
                room1 += 1
                if room1 > 5:
                    print("=== ERROR: number of people in room1:", room1, "===")
                    error = True
            elif "Left first room" in i:
                room1 -= 1
            elif "Joined the waiting room for second room" in i:
                waiting_room2 += 1
                if waiting_room2 > 2:
                    print("=== ERROR: number of people in waiting room:", waiting_room2, "===")
                    error = True
            elif "Entered second room" in i:
                if waiting_room2 > 0:
                    waiting_room2 -= 1
                room2 += 1
                if room2 > 2:
                    print("=== ERROR: number of people in room2:", room2, "===")
                    error = True
            elif "Left second room" in i:
                room2 -= 1
            elif "waiting room is full" in i:
                unhappy += 1
                if waiting_room2 < 2:
                    print("=== ERROR: waiting room was not full:", waiting_room2, "===")
                    error = True
            elif "Everything finished" in i:
                final_number = int(re.findall(r'\d+', i)[0])
                continue
            else:
                print("unknown output:", i)

        if final_number > 6 or 3 > final_number:
            print("number of unhappy customers is sus:", final_number)

        if not error:
            print("\noutput correct!")
        else:
            print("please make sure not to touch the print statements it breaks the autograder if you change it :'c")
        self.assertTrue(not error)

    def test_tunnel_output(self):
        print("======output checking=======")
        output = tunnel_output["output"].split('\n')
        if len(output) <= 0:
            print("no output!!?!")
            self.assertTrue(False)
            return
        error = False
        EW_num = 0
        WE_num = 0
        Ambulances_inside = 0
        for i in output[:-1]:
            print(i)
            # for cars
            if "Car" in i:
                if "entered tunnel in EW" in i:
                    if Ambulances_inside > 0:
                        print("=== ERROR", "===")
                        error = True
                    EW_num += 1
                elif "exited tunnel in EW" in i:
                    EW_num -= 1
                elif "entered tunnel in WE" in i:
                    if Ambulances_inside > 0:
                        print("=== ERROR", "===")
                        error = True
                    WE_num += 1
                elif "exited tunnel in WE" in i:
                    WE_num -= 1
                else:
                    print("unknown output", i)
            # for ambulance
            elif "Ambulance" in i:
                if "entered the tunnel in EW" in i:
                    Ambulances_inside += 1
                    EW_num += 1
                elif "exited the tunnel in EW" in i:
                    Ambulances_inside -= 1
                    EW_num -= 1
                elif "entered the tunnel in WE" in i:
                    Ambulances_inside += 1
                    WE_num += 1
                elif "exited the tunnel in WE" in i:
                    Ambulances_inside -= 1
                    WE_num -= 1
                else:
                    print("unknown output:", i)
            if EW_num > 3:
                print("=== ERROR", "===")
                error = True
            if WE_num > 1:
                print("=== ERROR", "===")
                error = True

        if not error:
            print("\noutput correct!")
        else:
            print("please make sure not to touch the print statements it breaks the autograder if you change it :'c")
        self.assertTrue(not error)

if __name__ == '__main__':
    unittest.main()
