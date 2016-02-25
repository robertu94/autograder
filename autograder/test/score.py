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

def score(settings, result, output, test):
    """
    Calculate a final score
    """
    scorers = {
        'passfail': score_passfail,
        'points': score_point,
        'script': score_script
        }
    return scorers[settings['tests'][test]['score']['method']](settings, result, output, test)

def score_point(settings, result, output, test):
    """
    Calculate a pass fail score
    """
    passed = int(result['passed'])
    extra = int(settings['tests'][test]['score']['free_points'])
    min_score = int(settings['tests'][test]['score']['min_points'])
    points_possible = int(settings['tests'][test]['score']['points_possible'])
    points_each = int(settings['tests'][test]['score']['points_each'])
    earned_score = min(max(min_score, points_each * passed + extra), points_possible)

    return {'earned': int(earned_score), 'possible':  int(points_possible)}

def score_passfail(settings, result, output, test):
    """
    Calculate a pass fail score
    """
    passed = int(result['passed'])
    min_score = int(settings['tests'][test]['score']['min_points'])
    points_possible = int(settings['tests'][test]['score']['points_possible'])
    if passed == points_possible:
        return {'earned': int(points_possible), 'possible':  int(points_possible)}
    else:
        return {'earned': int(min_score), 'possible':  int(points_possible)}


def score_script(settings, result, output, test):
    """
    Calculate a score using a script
    """
    cmd = settings['tests'][test]['score']['command']
    obj = {
        "run": output,
        "result": result
        }
    cmd_input = json.dumps(obj)
    ret = run.run_cmd(cmd, cmd_input)
    tmp = json.loads(ret['stdout'])
    points_earned, points_possible = tmp['earned'], tmp['possible']
    return {'earned': int(points_earned), 'possible':  int(points_possible)}

