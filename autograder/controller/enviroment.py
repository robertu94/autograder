#!/usr/bin/env python3

"""
This module is part of the Clemson ACM autograder

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


This module will prepare the testing environment
"""
import os
from autograder.source import build
from autograder.source import clean
from autograder.source import clone
from autograder.source import update

def prepare_enviroment(settings):
    """
    Prepares the environment that will be used for testing
    """
    if not os.path.exists(settings['project']['testdir']):
        clone_enviroment(settings)
    clean_enviroment(settings)
    update_enviroment(settings)
    build_enviroment(settings)

def clean_enviroment(settings):
    """
    Clean the environments used to grade the projects

    dict settings - the return value from parse_args
    """
    project = {
        "directory": settings['project']['testdir'],
        "username": settings['project']['testdir']
    }
    setting = settings['project']['enviroment']
    return clean.clean(setting, project)

def build_enviroment(settings):
    """
    Build the programs used to grade the projects

    dict settings - the return value from parse_args
    """
    project = {
        "directory": settings['project']['testdir'],
        "username": settings['project']['testdir']
    }
    setting = settings['project']['enviroment']
    return build.build(setting, project, building_test_cases=True)

def update_enviroment(settings):
    """
    update the programs used to grade the projects

    dict settings - the return value from parse_args
    """
    project = {
        "directory": settings['project']['testdir'],
        "username": settings['project']['testdir']
    }
    setting = settings['project']['enviroment']
    return update.update(setting, project)

def clone_enviroment(settings):
    """
    clone the programs used to grade the projects

    dict settings - the return value from parse_args
    """

    project = {
        "directory": settings['project']['testdir'],
        "username": settings['project']['testdir']
    }
    setting = settings['project']['enviroment']
    return clone.clone(setting, project)
