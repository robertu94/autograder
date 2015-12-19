#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader


This module is responsible for cloning and updating repositories.
"""
import logging
LOGGER = logging.getLogger(__name__)

def update(settings, student):
    """
    Updates a to the latest student submission
    return:
        bool updated - whether or not changes were made to the repository
    """
    updaters = {
        "git": update_git,
        "hg" : update_hg,
        "noop": update_noop,
        "svn": update_svn,
        "script": update_script
    }
    return updaters[settings.update.method](settings, student)


def update_hg(settings, student):
    """
    Updates a Mercurial repository with the latest submission
    """
    LOGGER.info('Beginning a HG update for student %s', student['username'])
    #hg incoming //check for updates
    #hg pull
    #hg update --clean


def update_git(settings, student):
    """
    Updates a Git repository with the latest submission
    """
    LOGGER.info('Beginning a git update for student %s', student['username'])
    pass

def update_noop(settings, student):
    """
    A No-Op updater
    """
    LOGGER.info('Beginning a NOOP update for student %s', student['username'])
    return True

def update_svn(settings, student):
    """
    Updates a SVN repository with the latest submission
    """
    LOGGER.info('Beginning a svn update for student %s', student['username'])

def update_script(settings, student):
    """
    Updates a SVN repository with the latest submission
    """
    LOGGER.info('Beginning a script update for student %s', student['username'])
    #./scipt student

