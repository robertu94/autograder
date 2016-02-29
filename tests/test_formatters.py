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

This module contains the functions related to formatters
"""
import json
import unittest

from autograder.report import formatters

class FormattersTest(unittest.TestCase):
    """
    Tests that ensure that results are formatted correctly
    """
    def setUp(self):
        self.maxDiff = None
        with open("resource/results.json") as infile:
            self.sample_results = json.load(infile)

    def test_format_machine_class_summary(self):
        """
        Method that tests the format_machine_class_summary method
        """
        expected = {
            "stdout": "this is the stdout1\nthis is the stdout2\nthis is the stdout1 bar\nthis is the stdout2 wrong\n",
            "stderr": "this is the stderr1\nthis is the stderr2\nthis is the stderr1 foo\nthis is the stderr2 wrong\n",
            "return": 0,
            "time": 4.9,
            "error": 0,
            "passed": 23,
            "failed": 9,
            "skipped": 0,
            "errors": 0,
            "total": 32,
            "earned": 23,
            "possible": 32
        }
        ret = formatters.format_machine_class_summary(["output", "results", "points"], self.sample_results)
        self.assertEqual(ret, expected)


    def test_format_class_summary(self):
        """
        Method that tests the format_machine_class_summary method
        """
        expected = (
            "earned: 23\n"
            "error: 0\n"
            "errors: 0\n"
            "failed: 9\n"
            "passed: 23\n"
            "possible: 32\n"
            "return: 0\n"
            "skipped: 0\n"
            "stderr: this is the stderr1\nthis is the stderr2\nthis is the stderr1 foo\nthis is the stderr2 wrong\n\n"
            "stdout: this is the stdout1\nthis is the stdout2\nthis is the stdout1 bar\nthis is the stdout2 wrong\n\n"
            "time: 4.9\n"
            "total: 32\n"
        )
        ret = formatters.format_class_summary(["output", "results", "points"], self.sample_results)
        self.assertEqual(ret, expected)

    def test_format_student_summary(self):
        """
        Method that tests the format_machine_student_summary method
        """
        expected = (
            "earned: 14\n"
            "error: 0\n"
            "errors: 0\n"
            "failed: 2\n"
            "passed: 14\n"
            "possible: 16\n"
            "return: 0\n"
            "skipped: 0\n"
            "stderr: this is the stderr1\nthis is the stderr2\n\n"
            "stdout: this is the stdout1\nthis is the stdout2\n\n"
            "time: 2.4\n"
            "total: 16\n"
        )
        student = self.sample_results['student1']
        ret = formatters.format_student_summary(["output", "results", "points"], student)
        self.assertEqual(ret, expected)

    def test_format_machine_student_summary(self):
        """
        Method that tests the format_machine_student_summary method
        """
        expected = {
            "stdout": "this is the stdout1\nthis is the stdout2\n",
            "stderr": "this is the stderr1\nthis is the stderr2\n",
            "return": 0,
            "time": 2.4,
            "error": 0,
            "passed": 14,
            "failed": 2,
            "skipped": 0,
            "errors": 0,
            "total": 16,
            "earned": 14,
            "possible": 16
        }
        student = self.sample_results['student1']
        ret = formatters.format_machine_student_summary(["output", "results", "points"], student)
        self.assertEqual(ret, expected)

    def test_format_test_case(self):
        """
        Method that tests the format_test_case method
        """
        expected = ("stdout: b'this is the stdout1\\n'\n"
                    "stderr: b'this is the stderr1\\n'\n"
                    "return: 0\n"
                    "time: 1.2\n"
                    "error: False\n"
                    "passed: 7\n"
                    "failed: 1\n"
                    "skipped: 0\n"
                    "errors: 0\n"
                    "total: 8\n"
                    "earned: 7\n"
                    "possible: 8\n")
        test_case = self.sample_results['student1'][0]
        ret = formatters.format_test_case(["output", "results", "points"], test_case)
        self.assertEqual(ret, expected)


    def test_format_machine_test_case(self):
        """
        Method that tests the format_machine_test_case method
        """
        expected = self.sample_results['student1'][0]
        test_case = self.sample_results['student1'][0]
        ret = formatters.format_machine_test_case(['output', 'results', 'points'], test_case)
        self.assertEqual(ret, expected)

    def test_format_machine_test_case_flat(self):
        """
        Method that tests the format_machine_test_case method
        """
        expected = {
            "stdout": "this is the stdout1\n",
            "stderr": "this is the stderr1\n",
            "return": 0,
            "time": 1.2,
            "error": False,
            "passed": 7,
            "failed": 1,
            "skipped": 0,
            "errors": 0,
            "total": 8,
            "earned": 7,
            "possible": 8
        }
        test_case = self.sample_results['student1'][0]
        ret = formatters.format_machine_test_case_flat(['output', 'results', 'points'], test_case)
        self.assertEqual(ret, expected)

    def test_format_test_case_output(self):
        """
        Method that tests the format_test_case_output method
        """
        expected = ("stdout: b'this is the stdout1\\n'\n"
                    "stderr: b'this is the stderr1\\n'\n"
                    "return: 0\n"
                    "time: 1.2\n"
                    "error: False\n")
        test_case = self.sample_results['student1'][0]
        ret = formatters.format_test_case_output(test_case)
        self.assertEqual(ret, expected)


    def test_format_test_case_results(self):
        """
        Method that tests the format_test_case_results method
        """
        expected =("passed: 7\n"
                   "failed: 1\n"
                   "skipped: 0\n"
                   "errors: 0\n"
                   "total: 8\n")
        test_case = self.sample_results['student1'][0]
        ret = formatters.format_test_case_results(test_case)
        self.assertEqual(ret, expected)
    
    def test_format_test_case_points(self):
        """
        Method that tests the format_test_case_points method
        """
        expected = ("earned: 7\n"
                    "possible: 8\n")
        test_case = self.sample_results['student1'][0]
        ret = formatters.format_test_case_points(test_case)
        self.assertEqual(ret, expected)
