#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for reporting student results in several different
formats.
"""
import logging
LOGGER = logging.getLogger(__name__)

def report(settings, report_id, results):
    """
    Generate a variety of reports based on the data
    """
    reporters = {
        'text' : report_text,
        'email' : report_email,
        'json' : report_json,
        'csv' : report_csv,
        'script' : report_script,
    }
    reporters[settings['reports'][report_id]['method']](settings, report_id, results)

def _report(settings, report, results):
    """
    Backend that implements the various reporting modules
    """
    seperate = settings["reports"][report]["seperate"]
    if seperate:
        for student in results:
            generated_report = generate_report(results[student])
            send_report(generated_report)
    else:
        generated_report = "".join([generate_report(results[student]) for student in results])
        send_report(generated_report)

def send_report(dictionary):
    """
    input: text
    output: none
    actions:
            -> sends report out to email
            -> saves report to file
            -> outputs report to stdout
    """
    return dictionary

def generate_report(student_results):
    """
    Generate_report
            input: dictionary containing 1 students results
            output: text
            actions:
                    -> take the dictionary and generate a human readable or machine readable report
                            -> csv, json
                            -> text
                    -> filter out unnecessary sections
    """
    return str(student_results)


