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

It is responsible for building projects that will be graded and Grader programs
"""
import logging
import subprocess
import shutil
import os

LOGGER = logging.getLogger(__name__)

def build(settings, student, building_test_cases=False):
    """
    Build the files that were submitted
    """
    builder = {
        'script': build_script,
        'make': build_make,
        'docker': build_docker,
        'noop': build_noop
        }
    if not building_test_cases:
        build_prepare(settings, student)
    try:
        builder[settings['build']['method']](settings, student)
    except subprocess.CalledProcessError:
        LOGGER.warning("build for student %s failed" % student['username'])

def build_prepare(settings, student):
    """
    Copies the tests intro the autograder directory
    """
    auto_grader_directory = os.path.join(student['directory'], '.autograder')
    try:
        shutil.rmtree(auto_grader_directory)
    except FileNotFoundError:
        pass #autograder files may not exist yet
    shutil.copytree(settings['project']['testdir'], auto_grader_directory)


    #Copy the docker ignore file
    try:
        studentdir = os.path.join(student['directory'], settings['build']['dockerignore'])
    except KeyError:
        pass
    else:
        shutil.copy(studentdir, student['directory'])


def build_script(settings, student):
    """
    A convince command that allows for building using a script.
    """
    LOGGER.info('Beginning a Script build for student %s', student['username'])
    cmd = settings['build']['command']
    timeout = int(settings['build']['timeout']) or 5
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          shell=True, timeout=timeout, cwd=student['directory'])

    LOGGER.info('Completed a Script build for student %s', student['username'])

def build_make(settings, student):
    """
    A convince command that allows for building using a makefile.
    """
    LOGGER.info('Beginning a Make build for student %s', student['username'])
    cmd = 'make'
    timeout = int(settings['build']['timeout']) or 5
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          timeout=timeout, cwd=student['directory'])

    LOGGER.info('Completed a Make build for student %s', student['username'])

def build_docker(settings, student):
    """
    Creates a new docker container for the student
    """
    LOGGER.info('Beginning a Docker build for student %s', student['username'])



    cmd = 'docker build -t {student}_{project} --file={dockerfile} .'
    cmd = cmd.format(student=student['username'], project=settings['project']['name'],
                     dockerfile=settings['build']['dockerfile'])
    timeout = settings['build']['timeout']

    LOGGER.info(cmd)

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                          timeout=timeout, cwd=student['directory'])
    LOGGER.info('Completed a Docker build for student %s', student['username'])

def build_noop(settings, student):
    """
    Build action that is a noop
    """
    pass
