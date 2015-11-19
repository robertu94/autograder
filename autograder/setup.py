#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for parsing settings and building tests if necessary.
This module also configures logging


settings:
    project:
        method - method of enumerating class. It can be one of {"discover","file","manual"}
        file - if method is "file" the list of list of student usernames
        student - if method is "manual" the username of the student to test
        name - name of the project
        testdir - directory of files that should be copied into the build
            directory.  They will be copied into a '.autograder' directory at the
            root of the repository.
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
                {"bats","unittest","script","docker"}
            command - when run method is "script" the command to use to run
                      this must output one of the passable formats
        parse:
            method - type of parsing to preform. It can be one of
                {"json","csv","ini","tap","script"}
            command - when grade method is "script" the command to use
                to parse results must output json
        score:
            method - how to score the parsed results. It can be
                one of {"passfail","pass","script"}
            command - when score method is "script" the command
                to use to parse results must output two integers
                      separated by a space indicating points earned points possible
    reports[] - a list of one or more reporting tasks
        method - types of reporting to preform. It can be one of {"email","json","csv","script"}
        command - when the reporting method is "script" the command use to report the output
        detail - amount of detail to report. It is a list that can
            contain {"output","result","score"}
    logging
        logfile - where output should be logged to disk
        file_verbosity - what level of output to show in the logfile
        console_verbosity - what level of output to show to the console
"""
import json
import logging
LOGGER = logging.getLogger(__name__)

def parse_settings(options):
    """
    Read in additional settings from a specified settings file

    namespace options - the return value from parse_args
    returns dict settings
    """
    settings = json.load(options.config_file)

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


def prepare_enviroment(settings):
    """
    Clean up the testing environment so tests are independent

    dict settings - the return value from parse_args
    """
    pass

def build_tests(settings):
    """
    Build the programs used to grade the projects

    dict settings - the return value from parse_args
    """
    pass

