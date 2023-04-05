import unittest
import random
from gradescope_utils.autograder_utils.decorators import leaderboard


class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        pass

    @leaderboard("high score")
    def test_leaderboard_float(self, set_leaderboard_value=None):
        """Sets a leaderboard value"""
        set_leaderboard_value(59.1)
