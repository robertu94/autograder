"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for testing the run functionality
"""

import subprocess
import unittest
from unittest import mock

from autograder.test import run

class RunTest(unittest.TestCase):
    """
    Tests that verify the run functionality
    """

    def setUp(self):
        """
        Create required mocks
        """
        patcher = mock.patch.object(run.subprocess.Popen, 'communicate', autospec=True)
        self.mock_popen = patcher.start()
        self.addCleanup(patcher.stop)

    def test_cmd(self):
        """
        Test running a script
        """
        self.mock_popen.return_value = ("stdout", "stderr")
        ret = run.run_cmd("foobar", "input", "/does/not/exist")
        expected = {
            "stdout": "stdout",
            "stderr": "stderr",
            "return": 0,
            "time": "stdout",
            "error": False,
        }
        self.assertEqual(expected, ret)

    def test_cmd_timeout(self):
        """
        Test running a script
        """
        self.mock_popen.side_effect = [
            subprocess.TimeoutExpired("foobar", 5), ("stdout", "stderr")
        ]
        ret = run.run_cmd("foobar")
        expected = {
            "stdout": "stdout",
            "stderr": "stderr",
            "return": 0,
            "time": "stdout",
            "error": True,
        }
        self.assertEqual(expected, ret)

    def test_cmd_directory_does_not_exist(self):
        """
        Running a command in a directory that does not exist
        """
        with self.assertRaises(FileNotFoundError):
            run.run_cmd("foobar", cwd="/does/not/exist")

    def test_script(self):
        """
        Test running a script
        """
        self.mock_popen.return_value = ("stdout", "stderr")
        ret = run.run_script()

    def test_script_timeout(self):
        """
        Test running a script that times out
        """

        self.mock_popen.side_effect = [
            subprocess.TimeoutExpired("foobar", 5), ("stdout", "stderr")
        ]
        ret = run.run_script()

