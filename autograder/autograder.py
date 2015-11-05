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
    parser = argparse.ArgumentParser(prog="Auto Grader")
    return parser.parse_args()
