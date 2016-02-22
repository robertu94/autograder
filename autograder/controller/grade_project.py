#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module provides utilities that allow for enumerating through student
submissions.
"""
import os
import logging
from autograder.source import build, clean, clone, update
from autograder.report import reports
from autograder.test import run, score, parse
LOGGER = logging.getLogger(__name__)

def grade(settings):
    """
    Grade all of the projects
    """
    results = {}
    for student in enumerate_students(settings):
        result = grade_student(settings, student)
        results[student] = result
    for report in enumerate_reports(settings):
        reports.report(settings, report, results)

def grade_student(settings, student):
    """
    Grade student a specific students work
    """
    if not os.path.exists(student['directory']):
        clone.clone(settings, student)
    clean.clean(settings, student)
    update.update(settings, student)
    results = []
    for test in enumerate_tests(settings):
        result = run_test(settings, student, test)
        results.insert(result)
    return results

def enumerate_reports(settings):
    """
    Returns a list of all reports that can be detected for the project

    return:
        reports[] - list of reports that will be produced
    """
    pass


def enumerate_students(settings):
    """
    Returns a list of all students that can be detected for the project

    return:
        students[] - list of students that will be graded
    """
    pass

def enumerate_tests(settings):
    """
    Returns a list of all tests that can be detected for the project

    return:
        tests[] - list of tests that will be run
    """
    pass

def run_test(settings, student, test):
    """
    Run a test on a students work
    """
    clean.clean(settings, student)
    build.build(settings, student)
    output = run.run(settings, student, test)
    result = parse.parse(settings, output, test)
    points = score.score(settings, result, output, test)
    return {
        "output": output,
        "result": result,
        "points": points
    }
