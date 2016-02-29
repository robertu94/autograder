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

This module contains the functions related to build
"""
import subprocess
import unittest
from unittest import mock

from autograder.source import build

class TestBuild(unittest.TestCase):
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


