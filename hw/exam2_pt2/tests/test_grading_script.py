import os
import sys
import subprocess
import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, number, partial_credit

sys.path.insert(0, '../..')  # adds the hw project dir to the python path

os.chdir('src')


class TestIntegration(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0)
    @number("1")
    def test_coffee_pot(self):
        """autograder coffee_pot"""
        rez = subprocess.run("./coffee_pot.bin".split(), capture_output=True, text=True, timeout=10)
        print(rez.stdout)
        self.assertTrue(True)

    @weight(0)
    @number("2")
    def test_relay_race(self):
        """autograder relay_race"""
        rez = subprocess.run("./relay_race.bin".split(), capture_output=True, text=True, timeout=10)
        print(rez.stdout)
        self.assertTrue(True)

    @weight(0)
    @number("3")
    def test_marcopolo(self):
        """autograder marcopolo"""
        rez = subprocess.run("./marcopolo.bin".split(), capture_output=True, text=True, timeout=10)
        print(rez.stdout)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
