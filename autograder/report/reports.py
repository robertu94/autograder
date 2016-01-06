#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for reporting student results in several different
formats.
"""
import json
import logging
import smtplib
LOGGER = logging.getLogger(__name__)

def report(settings, report, results):
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
    reporters[settings['reports'][report]['method']](settings, report, results)

def report_text(settings, results):
    """
    Generate a variety of reports based on the data and email it out
    """
    dest = settings['report'][report]
    message = format_human_report(settings['report'][report]['detail'], results)

    with open(dest, 'w') as outfile:
        outfile.write(message)

def report_email(settings,report, results):
    """
    Generate a variety of reports based on the data and email it out
    """
    from_address = settings['report'][report]['from']
    to_address = settings['report'][report]['to']
    message = format_human_report(settings['report'][report]['detail'], results)

    with smtplib.SMTP('localhost') as mailer:
        mailer.sendmail(from_address, to_address, message)



def report_json(settings, report, results):
    """
    Generate a variety of reports based on the data and format it in JSON
    """
    dest = settings['report'][report]
    message = format_human_report(settings['report'][report]['detail'], results)

    with open(dest, 'w') as outfile:
        json.dump(message, outfile)

def report_csv(settings, report, results):
    """
    Generate a variety of reports based on the data and format it in csv
    """
    raise NotImplementedError

def report_script(settings, report, results):
    """
    Generate a variety of reports based on the data and format it using a custom script
    """
    pass

def format_human_report(detail, results):
    """
    Generate a string that will be used in the final report
    params:
        str detail - the level of detail for the report
        str results - the results to be reported
    """
    FORMAT = {
        "output": format_output,
        "result": format_result,
        "score": format_score
        }
    return "".join([FORMAT[key](results) for key in results if key in detail])


def format_machine_report(detail, results):
    """
    for the dictionary based reporting styles (json,csv) generate the
    dictionary that will returned in the final report
    params:
        str detail - the level of detail for the report
        str results - the results to be reported
    """
    return {key:results[key] for key in results if key in detail}

def format_output(results):
    """
    format the output section in a human readable format
    """
    output = results["output"]
    return """stdout: {{stdout}}
    stderr: {{stderr}}
    return: {{returncode}}
    time: {{time}}
    error: {{error}}
    """.format(stdout=output['stdout'], stderr=output['stderr'],
               returncode=output['return'], time=output['time'],
               error=output['error'])

def format_result(results):
    """
    format the results section in a human readable format
    """
    result = results["result"]
    return """passed: {{passed}}
    failed: {{failed}},
    skipped: {{error}},
    total: {{total}}
    """.format(passed=result['passed'], failed=result['failed'],
               skipped=result['skipped'], total=result['total'])

def format_score(results):
    """
    format the score section in a human readable format
    """
    score = results["score"]
    return "{{earned}}/{{possible}}".format(earned=score['earned'], possible=score['possible'])

def transform_dest(settings, dest):
    """
    transform the destination address to use format codes
    """
    user = "user"
    email = "email"
    dest = dest.replace('%u', user)
    dest = dest.replace('%e', email)
    return dest
