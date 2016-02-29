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

This module contains the functions related to score
"""
import json
import unittest
import unittest.mock as mock
from autograder.test import score

class TestScore(unittest.TestCase):
    """
    Test cases for test_score
    """

    def setUp(self):
        """
        Load testing resources
        """
        with open("resource/results.json") as infile:
            self.sample_results = json.load(infile)


    def test_score_point(self):
        """
        A function to test the score_point functionality
        """
        test = {"score": {
            "min_points" : 5,
            "free_points" : 5,
            "points_each" : 5,
            "points_possible" : 15
            }
        }
        output = self.sample_results['student1'][0]['output']

        results = {"passed": 3}
        expected = {"earned": 15, "possible": 15}
        ret = score.score_point(results, output, test)
        self.assertEqual(ret, expected)

        results = {"passed": 2}
        expected = {"earned": 15, "possible": 15}
        ret = score.score_point(results, output, test)
        self.assertEqual(ret, expected)

        results = {"passed": 1}
        expected = {"earned": 10, "possible": 15}
        ret = score.score_point(results, output, test)
        self.assertEqual(ret, expected)

        results = {"passed": 0}
        expected = {"earned": 5, "possible": 15}
        ret = score.score_point(results, output, test)
        self.assertEqual(ret, expected)


    def test_score_passfail(self):
        """
        A function to test the score_passfail functionality
        """
        test = {"score": {
            "min_points" : 5,
            "points_possible" : 16
            }
               }
        output = self.sample_results['student1'][0]['output']

        result = {"passed": 16}
        expected = {"earned": 16, "possible": 16}
        ret = score.score_passfail(result, output, test)
        self.assertEqual(ret, expected)

        result = {"passed": 15}
        expected = {"earned": 5, "possible": 16}
        ret = score.score_passfail(result, output, test)
        self.assertEqual(ret, expected)



    @mock.patch("autograder.test.parse.run.run_cmd")
    def test_score_script(self, run_patch):
        """
        A function to test the score_script functionality
        """
        test = {"score":{"command" : "cmd"}}
        output = self.sample_results['student1'][0]["output"]
        result = self.sample_results['student1'][0]["results"]
        expected_points = {"earned": 14, "possible": 16}
        cmd_input = json.dumps({"run": output, "result": result})

        run_patch.return_value = {"stdout": json.dumps(expected_points)}

        ret = score.score_script(result, output, test)

        run_patch.assert_called_with("cmd", cmd_input)
        self.assertEqual(ret, expected_points)


