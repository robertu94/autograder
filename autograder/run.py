#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for running tests
"""
import logging
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
    runners = {
        'script': run_script
        }
    runners[settings['tests'][test]['score']['method']](settings, student, test)

def run_script(settings, student, test):
    """
    Runs a script to execute a test
    """
    cmd = settings['tests'][test]['score']['command']
    cmd_input = settings['tests'][test]['score']['input']
    directory = student['directory']
    timeout = settings['tests'][test]['score']['timeout']
    stderr = STDERR[settings['tests'][test]['score']['stderr']]

    return run_cmd(cmd, cmd_input, directory, timeout, stderr)


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
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=cwd, stderr=stderr,
                               shell=True, stdin=subprocess.PIPE, universal_newlines=True)
    try:
        output, error = process.communicate(cmd_input, timeout)
        stoptime = time.time()
    except subprocess.TimeoutExpired:
        failed = True
        process.kill()
        output, error = process.communicate(cmd_input, timeout)
        stoptime = time.time()
    return {
        "return": process.returncode,
        "stdout": output,
        "stderr": error,
        "time": stoptime-starttime,
        "error": failed
        }
