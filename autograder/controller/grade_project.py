#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

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

This module provides utilities that allow for enumerating through student
submissions.

results structure:
{
	"student1": [
		{
			"output": {
				"stdout": "this is the stdout1\n",
				"stderr": "this is the stderr1\n",
				"return": 0,
				"time": 1.2,
				"error": false
			},
			"results": {
				"passed": 7,
				"failed": 1,
				"skipped": 0,
				"errors": 0,
				"total": 8
			},
			"points": {
				"earned": 7,
				"possible": 8
			}
		},
		{
			"output": {...},
			"results": {...},
			"points": {...}
		}
	],
        "student2": [...]
}

stdout - ASCII encoded string of the stdout of the process
stderr - ASCII encoded string of the stderr of the process
return - integer return code from the process
time - floating point value corresponding to the runtime
error - true if the process was killed/errored out
passed - integer number of test cases passed
failed - integer number of test cases failed
skipped - integer number of test cases skipped
errors - integer number of tests cases ending in an error
total - integer sum of the previous 4 values
earned - integers number of points earned
possible - integer number of points possible

students structure:
[
  {
    "directory": "example",
    "email": "example@foobar.com",
    "username": "example"
  },
  {...},
  ...
]

directory - string corresponding to the path to the repo on disk
email - string corresponding to the students email address
username - string corresponding to the students username
"""

import os
import logging
from autograder.source import build, clean, clone, update
from autograder.report import reports
from autograder.test import run, score, parse
from autograder.controller import enviroment, project
LOGGER = logging.getLogger(__name__)

def grade(settings):
    """
    Grade all of the projects
    """
    enviroment.prepare_enviroment(settings)
    students = project.enumerate_students(settings)
    results = {}
    for student in students:
        result = grade_student(settings, student)
        results[student['username']] = result
    for report in project.enumerate_reports(settings):
        reports.reports(report, results, students)

def grade_student(settings, student):
    """
    Grade student a specific students work
    """
    if not os.path.exists(student['directory']):
        clone.clone(settings, student)
    clean.clean(settings, student)
    update.update(settings, student)
    results = []
    for test in project.enumerate_tests(settings):
        result = run_test(settings, student, test)
        results.append(result)
    return results


def run_test(settings, student, test):
    """
    Run a test on a students work
    """
    clean.clean(settings, student)
    build.build(settings, student)
    output = run.run(settings, student, test)
    result = parse.parse(output, test)
    points = score.score(result, output, test)
    return {
        "output": output,
        "results": result,
        "points": points
    }
