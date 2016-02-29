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

This module contains the functions related to parse
"""
import json
import unittest
import unittest.mock as mock
from autograder.test import parse

class TestParse(unittest.TestCase):
    """
    Test cases for test_parse
    """
    def setUp(self):
        """
        Load testing resources
        """
        with open("resource/results.json") as infile:
            self.sample_results = json.load(infile)

        self.tap = []
        with open("resource/results1.tap") as infile:
            self.tap.append((json.load(infile),
                             {"passed":8, "failed":0, "skipped":0, "errors": 0, "total": 8}))
        with open("resource/results2.tap") as infile:
            self.tap.append((json.load(infile),
                             {"passed":2, "failed":6, "skipped":0, "errors": 0, "total": 8}))
        with open("resource/results3.tap") as infile:
            self.tap.append((json.load(infile),
                             {"passed":5, "failed":3, "skipped":0, "errors": 0, "total": 8}))

    @mock.patch("autograder.test.parse.run.run_cmd")
    def test_parse_script(self, run_patch):
        """
        A function to test the parse_script functionality
        """
        test = {"parse": {
            "command" : "cmd",
            "timeout" : 5
            }
               }
        output = self.sample_results['student1'][0]["output"]

        expected = {
            "passed": 14,
            "failed": 16,
            "skipped": 16,
            "errors": 16,
            "total": 16
        }
        cmd_input = output['stdout']

        run_patch.return_value = {"stdout": json.dumps(expected)}

        ret = parse.parse_script(output, test)

        run_patch.assert_called_with("cmd", cmd_input, timeout=5)
        self.assertEqual(ret, expected)

    def test_parse_tap(self):
        """
        A function to test the parse_tap functionality
        """
        test = None #ignored

        for i in self.tap:
            with self.subTest(i=i):
                ret = parse.parse_tap(i[0], test)
                self.assertEqual(ret, i[1])


