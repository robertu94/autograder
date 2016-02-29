#!/usr/bin/env python3
"""
This file is part to the Clemson ACM autograder

Copyright (c) 2016, Robert Underwood
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This module contains the functions related to run
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
        settings = None #ignored
        test = {
            'run': {
                "command": "./test_cmd.sh pass",
                "input": "timeout",
                "timeout": 1.0,
                "stderr": "yes"
            }
        }
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
        test = {
            'run': {
                "command": "./test_cmd.sh fail",
                "input": "timeout",
                "timeout": 1.0,
                "stderr": "yes"
            }
        }
        settings = None #ignored
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
        settings = None #ignored
        test = {
            'run': {
                "command": "./test_cmd.sh timeout",
                "input": "timeout",
                "timeout": 1.0,
                "stderr": "yes"
            }
        }
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

