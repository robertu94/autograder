#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for cleaning up the build environments
and other preparation tasks.
"""
import subprocess
import logging
LOGGER = logging.getLogger(__name__)

def clean(settings, student):
    """
    Removes all trace of a students work and creates a new sandbox for testing
    """
    preparer = {
        'script': clean_script,
        'git': clean_git,
        'hg': clean_hg,
        'svn': clean_svn,
        'noop': clean_noop,
        'docker': clean_docker,
        }
    preparer[settings['prepare']['method']](settings, student)

def clean_hg(settings, student):
    """
    cleans a Mercurial repository with the latest submission
    """
    LOGGER.info("Using hg to clean up the directory for student %s", student['username'])

    cmd = "hg purge --all --dirs --files"
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_git(settings, student):
    """
    cleans a Git repository with the latest submission
    """
    LOGGER.info("Using git to clean up the directory for student %s", student['username'])

    cmd = "git clean -xdf"
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_noop(settings, student):
    """
    A No-Op cleaner
    """
    LOGGER.info("Using the NOOP to clean up for student %s", student['username'])
    return True

def clean_svn(settings, student):
    """
    cleans a SVN repository with the latest submission
    """
    LOGGER.info("Using svn to clean up the directory")

    cmd = "svn revert"
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_script(settings, student):
    """
    cleans a script repository with the latest submission
    """
    LOGGER.info('Beginning a Script to clean up for student %s', student['username'])

    cmd = settings['prepare']['command']
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_docker(settings, student):
    """
    cleans a script repository with the latest submission
    """
    LOGGER.info('Beginning a docker clean up for student %s', student['username'])

    cmd = "docker rm {student}_{project}"
    cmd.format(studnet=student['username'], project=settings['project']['name'])
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

