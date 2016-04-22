#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

Copyright (c) 2016, Robert Underwood
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

This module is responsible for cleaning up the build environments
and other preparation tasks.

NOTE:
    The Version Control System based cleaners (svn,git,hg) will clean all
    directories except those that the version control system itself uses to
    track state('.svn','.git',and '.hg' respectfully).  If you are concerned
    about this possibility, use the script based cleaner.
"""
import subprocess
import logging
LOGGER = logging.getLogger(__name__)

def clean(settings, student):
    """
    Removes all trace of a students work and creates a new sandbox for testing
    """
    cleaner = {
        'script': clean_script,
        'git': clean_git,
        'hg': clean_hg,
        'svn': clean_svn,
        'noop': clean_noop,
        'docker': clean_docker,
        }
    cleaner[settings['clean']['method']](settings, student)

def clean_hg(settings, student):
    """
    cleans a Mercurial repository with the latest submission
    """
    LOGGER.info("Using hg to clean up the directory for student %s", student['username'])

    #Remove all untracked files and directories
    #Override all options to enable the purge extension to clean the directory
    cmd = "hg --config='extensions.purge=' purge --all --dirs --files"
    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    #Undo any changes to tracked files made since the last commit
    cmd = "hg update -C"
    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_git(settings, student):
    """
    cleans a Git repository with the latest submission
    """
    LOGGER.info("Using git to clean up the directory for student %s", student['username'])

    #Git by default will not clean sub directories that are also git repositories
    #Setting this option will force the directories to be cleaned
    force = settings['clean']['git']['force'] or False

    #First clean up untracked changes
    cmd = "git clean -xdf"

    if force:
        cmd += 'f'

    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    #Clean up tracked changes
    cmd = "git reset HEAD --hard"

    timeout = int(settings['clean']['timeout']) or 5

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
    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    #Clean up tracked changes
    cmd = "svn -R revert ."
    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_script(settings, student):
    """
    cleans a script repository with the latest submission
    """
    LOGGER.info('Beginning a Script to clean up for student %s', student['username'])

    cmd = settings['clean']['command']
    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

def clean_docker(settings, student):
    """
    cleans a script repository with the latest submission
    """
    LOGGER.info('Beginning a docker clean up for student %s', student['username'])

    cmd = "docker rm {student}_{project}"
    cmd = cmd.format(studnet=student['username'], project=settings['project']['name'])
    timeout = int(settings['clean']['timeout']) or 5

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

