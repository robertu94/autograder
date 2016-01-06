"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for testing the setup functionality
"""


import unittest

from autograder.controller import setup

class TestSetup(unittest.TestCase):
    """
    Test cases for the setup module
    """
    def test_merge(self):
        """
        Test the merge function
        """
        default = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                'e': 4,
                'f': "asdf",
                'g': {
                    "h": 5,
                    "i": "j",
                    },
                'j': 5,
                'k': "asdfasd"
                }
            }
        testing = {
            'a': 2,
            'd': {
                'e': 5,
                'f': "adsf",
                'k': "asdfasdfasdfadsf"
                }
            }
        expected = {
            'a': 2,
            'b': 2,
            'c': 3,
            'd': {
                'e': 5,
                'f': "adsf",
                'g': {
                    "h": 5,
                    "i": "j",
                    },
                'j': 5,
                'k': "asdfasdfasdfadsf"
                }
            }
        result = setup.merge(default, testing)
        self.assertEqual(expected, result)
