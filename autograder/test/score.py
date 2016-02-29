#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for grading student responses
"""
import json
import logging

from autograder.test import run
LOGGER = logging.getLogger(__name__)

def score(result, output, test):
    """
    Calculate a final score
    """
    LOGGER.debug(json.dumps(result, indent=2, sort_keys=True))
    scorers = {
        'passfail': score_passfail,
        'points': score_point,
        'script': score_script
        }
    return scorers[test['score']['method']](result, output, test)

def score_point(result, output, test):
    """
    Calculate a pass fail score
    """
    passed = int(result['passed'])
    extra = int(test['score']['free_points'])
    min_score = int(test['score']['min_points'])
    points_possible = int(test['score']['points_possible'])
    points_each = int(test['score']['points_each'])
    earned_score = min(max(min_score, points_each * passed + extra), points_possible)

    return {'earned': int(earned_score), 'possible':  int(points_possible)}

def score_passfail(result, output, test):
    """
    Calculate a pass fail score
    """
    passed = int(result['passed'])
    min_score = int(test['score']['min_points'])
    points_possible = int(test['score']['points_possible'])
    if passed == points_possible:
        return {'earned': int(points_possible), 'possible':  int(points_possible)}
    else:
        return {'earned': int(min_score), 'possible':  int(points_possible)}


def score_script(result, output, test):
    """
    Calculate a score using a script
    """
    cmd = test['score']['command']
    obj = {
        "run": output,
        "result": result
        }
    cmd_input = json.dumps(obj)
    ret = run.run_cmd(cmd, cmd_input)
    tmp = json.loads(ret['stdout'])
    points_earned, points_possible = tmp['earned'], tmp['possible']
    return {'earned': int(points_earned), 'possible':  int(points_possible)}

