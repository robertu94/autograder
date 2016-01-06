"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for testing the build functionality
"""


import subprocess
import unittest
from unittest import mock

from autograder.source import build

class BuildTests(unittest.TestCase):
    """
    A series of tests that validate the build functionality
    """

    def setUp(self):
        self.student = {
            'username': 'test',
            'directory': 'test/scratch'
            }

        self.settings = {
            'build': {
                'timeout': 5,
            },
            'project': {'name': 'testproject'}
        }

    @mock.patch('autograder.source.build.subprocess.check_call')
    def test_make(self, mock_check_call):
        """
        Test building a student project using make
        """
        build.build_make(self.settings, self.student)
        mock_check_call.assert_called_with('make', stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL, timeout=5,
                                           cwd=self.student['directory'])

    @mock.patch('autograder.source.build.subprocess.check_call')
    def test_script(self, mock_check_call):
        """
        Test cleaning up with a script
        """
        self.settings['build']['command'] = 'date'
        build.build_script(self.settings, self.student)
        mock_check_call.assert_called_with('date', stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL, shell=True, timeout=5,
                                           cwd=self.student['directory'])
