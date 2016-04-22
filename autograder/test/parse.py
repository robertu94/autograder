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

This module is responsible for parsing results from student submissions
"""
import json
import logging

from autograder.test import run
LOGGER = logging.getLogger(__name__)

def parse(output, test):
    """
    Method responsible for parsing the output of the test
    """
    LOGGER.debug(test['parse'])
    LOGGER.debug(json.dumps(output, indent=2, sort_keys=True))

    parser = {
        'tap': parse_tap,
        'script': parse_script
        }
    return parser[test['parse']['method']](output, test)

def parse_script(output, test):
    """
    parse output with a script
    """
    cmd = test['parse']['command']
    cmd_input = output['stdout']
    timeout = test['parse']['timeout']

    ret = run.run_cmd(cmd, cmd_input, timeout=timeout)

    return json.loads(ret['stdout'])

def parse_tap(output, test):
    """
    parse output from bats tap compliant mode
    """
    passed = 0
    failed = 0
    skipped = 0
    error = 0
    total = 0

    lines = output['stdout'].splitlines()
    try:
        _, total = lines[0].split('..')
    except IndexError:
        return {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "total": 0
        }

    total = int(total)

    for line in lines[1:]:
        if line.startswith("ok"):
            if "# skip" in line:
                skipped += 1
            else:
                passed += 1
        elif line.startswith("not ok"):
            failed += 1
    return {
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": error,
        "total": total
        }
