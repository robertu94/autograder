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

This module is responsible for running tests
"""
import logging
import signal
import subprocess
import time
LOGGER = logging.getLogger(__name__)
STDERR = {
    "yes": subprocess.PIPE,
    "no": subprocess.DEVNULL,
    "join": subprocess.STDOUT,
    "stdout": subprocess.STDOUT,
    "pipe": subprocess.PIPE,
    "devnull":subprocess.PIPE
    }

def run(settings, student, test):
    """
    Runs a script
    """
    LOGGER.debug(test['run'])
    runners = {
        'script': run_script,
        'docker': run_docker
        }
    return runners[test['run']['method']](settings, student, test)

def run_script(settings, student, test):
    """
    Runs a script to execute a test
    """
    cmd = test['run']['command']
    cmd_input = test['run']['input']
    directory = student['directory']
    timeout = test['run']['timeout']
    stderr = STDERR[test['run']['stderr']]

    return run_cmd(cmd, cmd_input, directory, timeout, stderr)

def run_docker(settings, student, test):
    """
    Runs a docker container to execute a test

    some constraints that may be useful include; See docker-run for more details
        --net=none <- disable networking
        --memory=1024m <- limit the guest to 1gb ram
        --memory-swap=1124m <- limit the guest's available swap to 100mb (1124m-1024m = 100m)
        --read-only <- make the root file system readonly
        --user <- set the user and group in the contianer (note you must create user/group)
        --ulimit <- set the ulimit in the container
        --device-read-iops=/dev/sda:1000 <- limit container to 1000 read operations per sec
        --device-write-iops=/dev/sda:1000 <- limit container to 1000 write operations per sec

    """
    student = student['username']
    project = settings['project']['name']
    command = test['run']['command']
    container = "{student}_{project}".format(student=student, project=project)
    cmd_input = test['run']['input']
    timeout = test['run']['timeout']
    #TODO eventually accept a dictionary instead of a sequence of flags
    constraints = test['run']['constraints']
    cmd = "docker run --rm {constraints} {container} {command}"
    cmd = cmd.format(command=command, container=container, constraints=constraints)
    LOGGER.debug(cmd)

    return run_cmd(cmd, cmd_input, timeout=timeout)


def run_cmd(cmd, cmd_input=None, cwd=None, timeout=5, stderr=subprocess.PIPE):
    """
    Internal run command that passes requested options

    params:
        str cmd - the command that should be executed
        str cmd_input - the input to pass to the command as a string
        str cwd - the directory to run the script from
        int timeout - the time to allow the script to run before terminating it
        stderr - Which output method to use can be one of subprocess.{PIPE, DEVNULL, STDOUT}
    return:
        dict process
            int return: int return code
            str stdout: the standard output from the script
            str stdout: the standard error from the script
            float time: the runtime for the script
            bool error: True if the command timed out.
    """

    failed = False
    starttime = time.time()
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=cwd, stderr=stderr,
                          shell=True, stdin=subprocess.PIPE, universal_newlines=True) as process:
        try:
            output, error = process.communicate(cmd_input, timeout)
            stoptime = time.time()
        except subprocess.TimeoutExpired:
            failed = True
            process.kill()
            try:
                output, error = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                output, error = "", ""
            stoptime = time.time()

    #POSIX specifies return negative the signal that killed the process if it was killed
    return {
        "return": process.returncode if process.returncode != None else  -signal.SIGKILL.value,
        "stdout": output,
        "stderr": error,
        "time": stoptime-starttime,
        "error": failed
        }
