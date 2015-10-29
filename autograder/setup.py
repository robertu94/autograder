#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for parsing settings and building tests if necessary.
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

