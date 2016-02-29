#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

Copyright (c) 2016, Robert Underwood
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This module is responsible for parsing settings and building tests if necessary.
This module also configures logging


settings:
    project:
        method - method of enumerating class. It can be one of {"discover","json","csv","manual"}
        file - if method is "csv" or "json" the list of list of student usernames
        student - if method is "manual" a json dictionary corresponding to the student
        name - name of the project
        testdir - directory of files that should be copied into the build
            directory.  They will be copied into a '.autograder' directory at the
            root of the repository.
        version - version of the settings module to use.  It should be an
            integer.  It will be incremented whenever a change is made to the json
            settings file interface
    prepare:
        method - type of clean to use. It can be one of {"git","hg","noop","svn","script", "docker"}
        command - when clean method is "script" the command to use to script
    update:
        method - type of update to use. It can be one of {"git","hg","noop","svn","script"}
        command - when update method is "script" the command to use to clean
    build:
        method - type of build method to use. It can be one of {"make","script","docker"}
        command - when build method is "script" the command to use to build
        timeout - how long to allow the build to run, 5 seconds if not specified.
        dockerfile - path to the dockerfile to be used in docker builds
    tests[] - a list of one or more test objects that contain
        run:
            method - type of grading to preform. It can be one of
                {"script","docker"}
            command - when run method is "script" the command to use to run
                      this must output one of the passable formats
            input - what input to pass to the script
            timeout - how long to run the test, 5 seconds if not specified.
            constraints - when run method "docker", a list of flags to pass to docker
                to limit resources
            stderr - how to handle standard error, it can be separate, combined
                with stdout, or dropped
        parse:
            method - type of parsing to preform. It can be one of
                {"tap","script"}
            input - when the parse method is script, what input format to use
                It can be one of {"json"}
            output - when the parse method is script, what output format to use
                It can be one of {"json"}
            command - when grade method is "script" the command to use
                to parse results
            timeout - how long to run the test, 5 seconds if not specified.
        score:
            method - how to score the parsed results. It can be
                one of {"passfail","points","script"}
            command - when score method is "script" the command
                to use to parse results must output two integers to stdout
                separated by a space indicating points earned and points possible
            input - when the parse method is script, what input format to use
                It can be one of {"json"}
            timeout - how long to run the test, 5 seconds if not specified.
            min_points - the minimum number of points that will be assigned for this section
            free_points - the number of points that are essentially extra
            points_possible - maximum number of points possible for this test
    reports[] - a list of one or more reporting tasks
        method - types of reporting to preform. It can be one of {}
        send_method - types of sending methods. It can be one of {"email","file"}
        source - where to send the report from output from for email
        destination - where to place the report.  For json and csv this should be a
            path, for email this should be an email address.
            This field can be expanded using the following format codes:
            '%e' the students email address
            '%u' the students username
            '%d' the date
        separate - true when that separate reports should be
            generated for each student
        subject - the subject when sent via email.
        command - when the reporting method is "script" the command use to report the output
        detail - amount of detail to report. It is a list that can
            contain {"output","result","score"}
        summarize - include the summary
    logging
        logfile - where output should be logged to disk
        file_verbosity - what level of output to show in the logfile
        console_verbosity - what level of output to show to the console
"""
import json
import logging
import logging.config

LOGGER = logging.getLogger(__name__)
DEFAULT_FILE = "/etc/autograder.conf"

def parse_settings(options):
    """
    Read in additional settings from a specified settings file

    namespace options - the return value from parse_args
    returns dict settings
    """
    settings = json.load(options.config_file)
    with open(DEFAULT_FILE) as default_config:
        defaults = json.load(default_config)
    settings = merge(defaults, settings)

    LOGGER.debug(json.dumps(settings, sort_keys=True, indent=2))

    return settings


def setup_logging(settings):
    """
    Setup logging for the Auto Grader

    dict settings - the return value from parse_args
    """
    logconfig = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
            },
            'simple' : {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console' : {
                'level': logging.getLevelName(settings['logging']['console_verbosity']),
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': settings['logging']['logfile'],
                'mode': 'a',
                'formatter': 'standard'
            },
        },
        'loggers': {
            'autograder': {
                'handlers': ['console'],
                'propagate' : True,
                'level': 'WARNING'
            },
            'autograder.grade_project': {
                'handlers': ['console', 'file'],
                'propagate' : False,
                'level': 'DEBUG'
            },
        },
    }

    logging.config.dictConfig(logconfig)

def merge(defaults, dictionary):
    """
    recursively merge two dictionaries
    """
    for item in defaults:
        try:
            if isinstance(dictionary[item], list):
                dictionary[item] = [merge(defaults[item], x) for x in dictionary[item]]
            elif isinstance(defaults[item], dict):
                dictionary[item] = merge(defaults[item], dictionary[item])
            else:
                dictionary[item] = dictionary.get(item, defaults[item])
        except KeyError:
            dictionary[item] = defaults[item]
    return dictionary


