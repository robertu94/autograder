#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is contains the main method for the module
"""
import argparse

from . import setup, grade_project

def main():
    """
    Main method for the autograder
    """
    options = parse_args()

    #Set up for the project
    settings = setup.parse_settings(options)
    setup.setup_logging(settings)
    setup.prepare_enviroment(settings)
    setup.build_tests(settings)

    #Grade the results
    grade_project.grade(settings)

def parse_args():
    """
    Parse the argument file for the appropriate options

    Command line options always override options in the config file
    """
    parser = argparse.ArgumentParser(prog="Auto Grader")
    parser.add_argument('config_file', type=argparse.FileType('r'),
                        help='A path to the main configuration file')
    return parser.parse_args()
