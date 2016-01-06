#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

It is responsible for building projects that will be graded and Grader programs
"""
import logging
import subprocess
import shutil
import os
LOGGER = logging.getLogger(__name__)

def build(settings, student):
    """
    Build the files that were submitted
    """
    builder = {
        'script': build_script,
        'make': build_make,
        'docker': build_docker
        }
    builder[settings['build']['method']](settings, student)

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

    cmd = 'docker build -t {student}_{project}'
    cmd = cmd.format(studnet=student['username'], project=settings['project']['name'])
    auto_grader_directory = os.path.join(student['directory'], '.autograder')
    timeout = int(settings['build']['timeout']) or None

    #prepare build directory
    shutil.copyfile(settings['build']['dockerfile'], student['directory'])
    shutil.rmtree(auto_grader_directory)
    shutil.copytree(settings['project']['testdir'], auto_grader_directory)


    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          timeout=timeout, cwd=student['directory'])
    LOGGER.info('Completed a Docker build for student %s', student['username'])

