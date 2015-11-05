#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for cleaning up the build environments
and other preparation tasks.
"""

def clean(settings, student):
    """
    Removes all trace of a students work and creates a new sandbox for testing
    """

def clean_hg(settings, student):
    """
    cleans a Mercurial repository with the latest submission
    """
    #hg update --clean
    pass

def clean_git(settings, student):
    """
    cleans a Git repository with the latest submission
    """
    #git clean -xdf
    pass

def clean_noop(settings, student):
    """
    A No-Op cleaner
    """
    return True

def clean_svn(settings, student):
    """
    cleans a SVN repository with the latest submission
    """

def clean_script(settings, student):
    """
    cleans a SVN repository with the latest submission
    """
    #./scipt student

