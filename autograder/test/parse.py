#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

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
