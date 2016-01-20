"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for testing the run functionality
"""

import signal
import unittest

from autograder.test import run

class RunTest(unittest.TestCase):
    """
    Tests that verify the run functionality
    """

    def test_cmd(self):
        """
        Test running a script
        """
        ret = run.run_cmd("./test_cmd.sh pass", "input", "./scripts")
        expected = {
            "stdout": "stdout\n",
            "stderr": "stderr\n",
            "return": 0,
            "time": 0.0,
            "error": False,
        }
        self.assert_similar_run_result(expected, ret)

    def test_cmd_timeout(self):
        """
        Test running a script
        """
        ret = run.run_cmd("./test_cmd.sh timeout", cwd="./scripts", timeout=1)
        expected = {
            "stdout": "stdout\n",
            "stderr": "stderr\n",
            "return": -9,
            "time": 1.0,
            "error": True,
        }
        self.assert_similar_run_result(expected, ret)

    def test_cmd_nonexistant_directory(self):
        """
        Running a command in a directory that does not exist
        """
        with self.assertRaises(FileNotFoundError):
            run.run_cmd("foobar", cwd="/does/not/exist")

    def test_script_pass(self):
        """
        Test running a script
        """
        settings = {
            "tests": [
                {
                    'score': {
                        "command": "./test_cmd.sh pass",
                        "input": "timeout",
                        "timeout": 1.0,
                        "stderr": "yes"
                    }
                }
            ]
        }
        test = 0
        student = {
            "directory": "scripts",
        }

        #Run test
        ret = run.run_script(settings, student, test)

        expected = {
            "stdout": "stdout\n",
            "stderr": "stderr\n",
            "return": 0,
            "time": 0.0,
            "error": False,
        }
        self.assert_similar_run_result(ret, expected)

    def test_script_fail(self):
        """
        Test running a script
        """
        settings = {
            "tests": [
                {
                    'score': {
                        "command": "./test_cmd.sh fail",
                        "input": "timeout",
                        "timeout": 1.0,
                        "stderr": "yes"
                    }
                }
            ]
        }
        test = 0
        student = {
            "directory": "scripts",
        }

        #Run test
        ret = run.run_script(settings, student, test)

        expected = {
            "stdout": "stdout\n",
            "stderr": "stderr\n",
            "return": 1,
            "time": 0.0,
            "error": False,
        }
        self.assert_similar_run_result(ret, expected)


    def test_script_timeout(self):
        """
        Test running a script that times out
        """
        #Configure input
        settings = {
            "tests": [
                {
                    'score': {
                        "command": "./test_cmd.sh timeout",
                        "input": "timeout",
                        "timeout": 1.0,
                        "stderr": "yes"
                    }
                }
            ]
        }
        test = 0
        student = {
            "directory": "scripts",
        }

        #Run test
        ret = run.run_script(settings, student, test)

        expected = {
            "stdout": "stdout\n",
            "stderr": "stderr\n",
            "return": -signal.SIGKILL.value,
            "time": 1.0,
            "error": True,
        }
        self.assert_similar_run_result(ret, expected)

    def assert_similar_run_result(self, expected, result):
        """
        Tests if the test results are similar to what is expected

        This method is necessary because the time element of scripts is
        non-deterministic.
        """
        self.assertEqual(expected['stdout'], result['stdout'])
        self.assertEqual(expected['stderr'], result['stderr'])
        self.assertEqual(expected['return'], result['return'])
        self.assertEqual(expected['error'], result['error'])
        self.assertAlmostEqual(expected['time'], result['time'], places=1)

