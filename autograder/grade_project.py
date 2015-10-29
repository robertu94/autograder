#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module provides utilities that allow for enumerating through student
submissions.
"""
def grade(settings):
    """
    Grade all of the projects
    """
    results = []
    for student in enumerate_students(settings)
        results.insert((student,grade_student()))
    report.report(results)

def grade_student(student):
    """
    Grade student a specific students work
    """
    prepare.clean()
    update.update()
    build.build()
    results = []
    for test in enumerate_tests(settings)
        results.insert(grade.grade())
    results = parse.parse(results)
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

