#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for reporting student results in several different
formats.
"""
import logging
from autograder.report import formatters, send

LOGGER = logging.getLogger(__name__)

def report(report, results, students):
    """
    Generate a variety of reports based on the data
    """
    if report['seperate']:
        for student in students:
            report_text = formatters.formatters(report, results, student)
            send.send(report, report_text, student)

    else:
        report_text = formatters.formatters(report, results)
        send.send(report, report_text)

