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


This module is contains the enumeration methods
"""
import csv
import json

def enumerate_reports(settings):
    """
    Returns a list of all reports that can be detected for the project

    return:
        reports[] - list of reports that will be produced
    """
    return settings['reports']

def enumerate_students(settings):
    """
    Returns a list of all students that can be detected for the project

    return:
        students[] - list of students that will be graded
    """
    STUDENTS = {
        "json": enumerate_students_json,
        "csv": enumerate_students_csv,
        "manual": enumerate_students_manual
    }
    return STUDENTS[settings['project']['method']](settings)

def enumerate_tests(settings):
    """
    Returns a list of all tests that can be detected for the project

    return:
        tests[] - list of tests that will be run
    """
    return settings['tests']

def enumerate_students_json(settings):
    """
    Return a list of students by reading a json file
    """
    with open(settings['project']['file']) as infile:
        students = json.load(infile)
    return students

def enumerate_students_csv(settings):
    """
    Return a list of students by reading a json file
    """
    students = []
    with open(settings['project']['file']) as infile:
        dialect = csv.Sniffer().sniff(infile.read(1024))
        infile.seek(0)
        reader = csv.DictReader(infile, dialect=dialect)
        for student in reader:
            students.append(student)
    return students

def enumerate_students_manual(settings):
    """
    returns a list of a single student
    """
    return json.loads(settings['project']['student'])

def enumerate_students_discover(settings):
    """
    Automatically determine students using when used with Handin
    """
    raise NotImplementedError

