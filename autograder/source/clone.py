#!/usr/bin/env python3

"""
This module is part of the Clemson ACM autograder

This module will download and clone source code repositories
"""

import subprocess

def clone(settings, student):
    """
    Clones settings from various source code repositories
    """
    BACKENDS = {
        "git": clone_git,
        "svn": clone_svn,
        "hg": clone_hg,
        "script": clone_script,
        "noop": clone_noop
        }
    BACKENDS[settings['clone']['method']](settings, student)

def clone_git(settings, student):
    """
    Clones from a git source code repository
    """
    timeout = settings['clone']['timeout']
    directory = student['directory']
    repo = student['repo']
    subprocess.check_call(["git", "clone", repo, directory], timeout=timeout,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clone_hg(settings, student):
    """
    Clones from a hg source code repository
    """
    timeout = settings['clone']['timeout']
    directory = student['directory']
    repo = student['repo']
    subprocess.check_call(["hg", "clone", repo, directory], timeout=timeout,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clone_svn(settings, student):
    """
    Clones from a svn source code repository
    """
    timeout = settings['clone']['timeout']
    directory = student['directory']
    repo = student['repo']
    subprocess.check_call(["svn", "checkout", repo, directory], timeout=timeout,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clone_script(settings, student):
    """
    Clones from a script source code repository
    """
    timeout = settings['clone']['timeout']
    cmd = settings['clone']['command']
    subprocess.check_call(cmd, shell=True, timeout=timeout,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clone_noop(settings, student):
    """
    Preform a noop for this stage
    """
    pass
