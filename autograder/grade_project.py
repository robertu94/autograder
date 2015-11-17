#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module provides utilities that allow for enumerating through student
submissions.
"""
import logging
LOGGER = logging.getLogger(__name__)

def grade(settings):
    """
    Grade all of the projects
    """
    results = {}
    for student in enumerate_students(settings):
        result = grade_student(settings, student)
        results[student] = result
    report.report(settings, results)

def grade_student(settings, student):
    """
    Grade student a specific students work
    """
    prepare.clean(settings, student)
    update.update(settings, student)
    build.build(settings, student)
    results = []
    for test in enumerate_tests(settings):
        result = run_test(settings, student, test)
        results.insert(result)
    return results



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
    prepare.clean(settings, student)
    output = run.run(student, test)
    result = parse.parse(output, test)
    score = grader.score(result, test)
    return output, result, score
