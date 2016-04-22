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
