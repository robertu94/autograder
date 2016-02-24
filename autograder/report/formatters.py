#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for formatting student results in several different
formats.
"""
import functools
import logging
import operator
LOGGER = logging.getLogger(__name__)

SUBHEADERS = {
    "output": ["stderr", "stdout", "return", "error", "time"],
    "points": ["earned", "possible"],
    "results":["errors", "passed", "failed", "skipped", "total"]
}

def format_machine_class_summary(detail, results):
    """
    Generates summary statistics for the entire class
    """
    result = {}
    summary = {}
    for student in sorted(results):
        result[student] = format_machine_student_summary(detail, results[student])
    for header in detail:
        for subheader in SUBHEADERS[header]:
            summary[subheader] = \
                functools.reduce(operator.add, [result[student][subheader] for student in sorted(result)])
    return dict(summary)


def format_class_summary(detail, results):
    """
    Used for creating a human readable summary of class's results
    """
    machine = format_machine_class_summary(detail, results)
    return "".join(["{field}: {value}\n".format(field=field, value=machine[field])
                    for field in sorted(machine)])


def format_student_summary(detail, results):
    """
    Used for creating a human readable summary of a single student's results
    """
    machine = format_machine_student_summary(detail, results)
    return "".join(["{field}: {value}\n".format(field=field, value=machine[field])
                    for field in sorted(machine)])

def format_machine_student_summary(detail, results):
    """
    Used for creating a human readable summary of a single students results
    """
    summary = {}
    for header in detail:
        for subheader in SUBHEADERS[header]:
            summary[subheader] = \
                functools.reduce(operator.add, [i[header][subheader] for i in results])
    return summary

def format_test_case(detail, results):
    """
    Generate a string that will be used in the final report
    params:
        str detail - the level of detail for the report
        str results - the results to be reported
    """
    FORMAT = {
        "output": format_test_case_output,
        "results": format_test_case_results,
        "points": format_test_case_points
        }
    return "".join([FORMAT[key](results) for key in detail])

def format_machine_test_case(detail, results):
    """
    for the dictionary based reporting styles (json) generate the
    dictionary that will returned in the final report
    params:
        str detail - the level of detail for the report
        str results - the results to be reported
    """
    return {key:results[key] for key in results if key in detail}

def format_machine_test_case_flat(detail, results):
    """
    for the list based reporting styles (csv) generate the
    dictionary that will returned in the final report
    params:
        str detail - the level of detail for the report
        str results - the results to be reported
    """
    summary = {}
    for header in detail:
        for subheader in SUBHEADERS[header]:
            summary[subheader] = results[header][subheader]
    return summary

def format_test_case_output(results):
    """
    format the output section in a human readable format
    """
    output = results["output"]
    return (
        "stdout: {stdout}\n"
        "stderr: {stderr}\n"
        "return: {returncode}\n"
        "time: {time}\n"
        "error: {error}\n"
        "".format(stdout=output['stdout'].encode("ascii"),
                  stderr=output['stderr'].encode("ascii"),
                  returncode=output['return'], time=output['time'],
                  error=output['error'])
        )

def format_test_case_results(results):
    """/format_test_case/g
    format the results section in a human readable format
    """
    result = results["results"]
    return (
        "passed: {passed}\n"
        "failed: {failed}\n"
        "skipped: {skipped}\n"
        "errors: {errors}\n"
        "total: {total}\n"
        "".format(passed=result['passed'], failed=result['failed'],
                  skipped=result['skipped'], total=result['total'],
                  errors=result['errors'])
    )

def format_test_case_points(results):
    """
    format the score section in a human readable format
    """
    score = results["points"]
    return (
        "earned: {earned}\n"
        "possible: {possible}\n"
        "".format(earned=score['earned'], possible=score['possible'])
    )

