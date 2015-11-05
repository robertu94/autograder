#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for parsing settings and building tests if necessary.


settings:
    project:
        method - method of enumerating class. It can be one of {"discover","file","manual"}
        file - if method is "file" the list of list of student usernames
        student - if method is "manual" the student to test
    prepare:
        method - type of clean to use. It can be one of {"git","hg","noop","svn","script"}
        command - when clean method is "script" the command to use to script
    update:
        method - type of update to use. It can be one of {"git","hg","noop","svn","script"}
        command - when update method is "script" the command to use to clean
    build:
        method - type of build method to use. It can be one of {"make","script"}
        command - when build method is "script" the command to use to build
    tests[] - a list of one or more test objects that contain
        run:
            method - type of grading to preform. It can be one of {"bats","unittest","script"}
            command - when run method is "script" the command to use to run
                      this must output one of the passable formats
        parse:
            method - type of parsing to preform. It can be one of {"json","csv","ini","tap","script"}
            command - when grade method is "script" the command to use to parse results must output json
        score:
            method - how to score the parsed results. It can be one of {"passfail","pass","script"}
            command - when grade method is "script" the command to use to parse results must output two integers
                      separated by a space indicating points earned points possible
    reports[] - a list of one or more reporting tasks
        method - types of reporting to preform. It can be one of {"email","json","csv","script"}
        command - when the reporting method is "script" the command use to report the output
        detail - amount of detail to report. It is a list that can contain {"output","result","score"}
    logging
        logfile - where output should be logged to disk
        file_verbosity - what level of output to show in the logfile
        console_verbosity - what level of output to show to the console
"""
from . import logging

def parse_settings(options):
    """
    Read in additional settings from a specified settings file

    namespace options - the return value from parse_args
    """
    pass

def setup_logging(settings):
    """
    Setup logging for the Auto Grader

    dict settings - the return value from parse_args
    """
    pass

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

