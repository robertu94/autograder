#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader


This module is responsible for cloning and updating repositories.
"""
import json
import logging
import subprocess
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
    return updaters[settings["update"]["method"]](settings, student)


def update_hg(settings, student):
    """
    Updates a Mercurial repository with the latest submission
    """
    LOGGER.info('Beginning a HG update for student %s', student['username'])
    timeout = int(settings['update']['timeout'])

    #Check if updates exist
    cmd = """
    hg incoming;
    """
    changed = False
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                              shell=True, timeout=timeout, cwd=student['directory'])
    except subprocess.CalledProcessError:
        changed = False

    #Download and apply updates
    cmd = """
    hg pull;
    hg update --clean;
    """
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    return changed


def update_git(settings, student):
    """
    Updates a Git repository with the latest submission
    """
    LOGGER.info('Beginning a git update for student %s', student['username'])
    timeout = int(settings['update']['timeout'])
    cmd = """
    git pull -f -Xtheirs;
    """
    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL,
                                  shell=True, timeout=timeout, cwd=student['directory'])
    return "Already up-to-date" in str(out)



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
    timeout = int(settings['update']['timeout'])

def update_script(settings, student):
    """
    Updates a SVN repository with the latest submission
    """
    LOGGER.info('Beginning a script update for student %s', student['username'])
    timeout = int(settings['update']['timeout'])
    cmd = settings['update']['method']
    output = subprocess.check_output(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])
    ret = json.loads(output)
    return ret['changed']


