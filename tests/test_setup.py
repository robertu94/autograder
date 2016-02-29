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

This module contains the functions related to setup
"""
import unittest
from autograder.controller import setup

class TestSetup(unittest.TestCase):
    """
    Test cases for test_setup
    """

    @unittest.skip("Unimplemented")
    def test_parse_settings (self):
        """
        A function to test the parse_settings functionality
        """
        pass

    @unittest.skip("Unimplemented")
    def test_setup_logging (self):
        """
        A function to test the setup_logging functionality
        """
        pass

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
                },
            'e': {
                'a': 1,
                'b': 2,
                'c': 3
                }
            }

        testing = {
            'a': 2,
            'd': {
                'e': 5,
                'f': "adsf",
                'k': "asdfasdfasdfadsf"
                },
            'e': [
                {'a': 3},
                {'b': 1},
                {'a': 3, 'b':3}

                ]
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
                },
            'e': [
                {'a': 3, 'b': 2, 'c': 3},
                {'a': 1, 'b': 1, 'c': 3},
                {'a': 3, 'b': 3, 'c': 3}
                ]
            }
        result = setup.merge(default, testing)
        self.assertEqual(expected, result)

    @unittest.skip("Unimplemented")
    def test_prepare_enviroment (self):
        """
        A function to test the prepare_enviroment functionality
        """
        pass

    @unittest.skip("Unimplemented")
    def test_build_tests (self):
        """
        A function to test the build_tests functionality
        """
        pass


