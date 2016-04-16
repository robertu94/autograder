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


This module is contains the Clemson Handin interaction
"""
import itertools
import os

import yaml

from autograder.source import clone, update

def clone_metadata(settings):
    """
    Clones metadata for the first time
    """
    discovery_settings = {
        "clone": {
            "timeout": None,
            "method": "hg"
        }
    }
    clone.clone(discovery_settings, settings['project']['discovery'])

def update_metadata(settings):
    """
    Clones metadata for the first time
    """
    discovery_settings = {
        "clone": {
            "method": "hg"
        }
    }
    update.update(discovery_settings, settings['project']['discovery'])

def discover(settings):
    """
    Discovers metadata from a Handin Repository
    """
    project_directory = settings['project']['discovery']['directory']
    assignment_name = settings['project']['discovery']['assignment']
    if os.path.exists(project_directory):
        clone_metadata(settings)
    else:
        update_metadata(settings)


    manifest_file = os.path.join(project_directory, "admin/manifest.yaml")
    assingment_manifest_file = os.path.join(project_directory, "admin/assignments",
                                            assignment_name + ".yaml")

    with open(manifest_file) as infile:
        manifest = yaml.load(infile)
    students_usernames = set(manifest['students'])

    with open(assingment_manifest_file) as infile:
        assignment_manifest = yaml.load(infile)

    shared_buckets_users = set(itertools.chain(
        *[assignment_manifest['buckets'][bucket] for bucket in assignment_manifest['buckets']]))
    ungrouped_students = students_usernames - shared_buckets_users

    student_objects = {}
    for student in ungrouped_students:
        student_objects[student] = student_from_username(settings, student, student)
    for bucket in assignment_manifest['buckets']:
        needs_grading = True
        for student in assignment_manifest['buckets'][bucket]:
            if student in student_objects:
                raise RuntimeError("Students must be uniquely mapped to a bucket")
            student_objects[student] = \
                    student_from_username(settings, bucket, student, needs_grading)
            needs_grading = False
    return student_objects

def student_from_username(settings, bucket_name, username, needs_grading=True):
    """
    Format student structures from usernames
    """
    directory = settings['project']['discovery']['directory']
    assignment = settings['project']['discovery']['assignment']
    domain = settings['project']['discovery']['domain']
    base_repo = settings['project']['discovery']['repo']

    return {
        "directory": os.path.join(directory, "assignment", assignment, username),
        "email": "{username}@{domain}".format(username=username, domain=domain),
        "username": username,
        "repo": os.path.join(base_repo, "assignment", assignment, bucket_name),
        "needs_grading": needs_grading
    }

