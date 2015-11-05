#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader


This module is responsible for cloning and updating repositories.
"""

def update(settings, student):
    """
    Updates a to the latest student submission
    return:
        bool updated - whether or not changes were made to the repository
    """
    UPDATERS = { "git": update_git,
                "hg" : update_hg,
                "noop": update_noop,
                "svn": update_svn,
                "script": update_script
               }
    return UPDATERS[settings.update.method](settings, student)


def update_hg(settings, student):
    """
    Updates a Mercurial repository with the latest submission
    """
    #hg incoming //check for updates
    #hg pull
    #hg update --clean


def update_git(settings, student):
    """
    Updates a Git repository with the latest submission
    """
    #git clean -xdf
    #git pull
    #git submodule init
    #git submodule update
    pass

def update_noop(settings, student):
    """
    A No-Op updater
    """
    return True

def update_svn(settings, student):
    """
    Updates a SVN repository with the latest submission
    """

def update_script(settings, student):
    """
    Updates a SVN repository with the latest submission
    """
    #./scipt student

