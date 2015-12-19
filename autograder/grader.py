#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for grading student responses
"""
import json
import logging

import run
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

def score_passfail(settings, result, output, test):
    """
    Calculate a pass fail score
    """
    passed = int(result['passed'])
    extra = int(settings['tests'][test]['score']['free_points'])
    min_score = int(settings['tests'][test]['score']['min_points'])
    points_possible = int(settings['tests'][test]['score']['points_possible'])
    earned_score = min(max(min_score, passed + extra), points_possible)

    return earned_score, points_possible

def score_point(settings, result, output, test):
    """
    Calculate a pass fail score
    """
    passed = int(result['passed'])
    min_score = int(settings['tests'][test]['score']['min_points'])
    points_possible = int(settings['tests'][test]['score']['points_possible'])
    if passed == points_possible:
        return points_possible, points_possible
    else:
        return min_score, points_possible


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
    points_earned, points_possible = ret['stdout'].split()
    return int(points_earned), int(points_possible)

