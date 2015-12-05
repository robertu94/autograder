#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for cleaning up the build environments
and other preparation tasks.

NOTE:
    The Version Control System based cleaners (svn,git,hg) will clean all
    directories except those that the version control system itself uses to
    track state('.svn','.git',and '.hg' respectfully).  If you are concerned
    about this possibility, use the soscript based preparer.
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

    #Remove all untracked files and directories
    #Override all options to enable the purge extension to clean the directory
    cmd = "hg --config='extensions.purge=' purge --all --dirs --files"
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    #Undo any changes to tracked files made since the last commit
    cmd = "hg update -C"
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_git(settings, student):
    """
    cleans a Git repository with the latest submission
    """
    LOGGER.info("Using git to clean up the directory for student %s", student['username'])

    #Git by default will not clean sub directories that are also git repositories
    #Setting this option will force the directories to be cleaned
    force = settings['prepare']['git']['force'] or False

    #First clean up untracked changes
    cmd = "git clean -xdf"

    if force:
        cmd += 'f'

    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    #Clean up tracked changes
    cmd = "git reset HEAD --hard"

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

    #Clean up up untracked files
    #TODO this can be done more cleanly and should remove dependencies on awk and xargs
    cmd = "svn st| awk '/?/ {print $2}'| xargs rm -rf"
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    #Clean up tracked changes
    cmd = "svn -R revert ."
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
    cmd = cmd.format(studnet=student['username'], project=settings['project']['name'])
    timeout = int(settings['prepare']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

