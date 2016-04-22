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

This module is responsible for reporting student results in several different
formats.
"""
import smtplib
import email
import datetime

def send(report, report_text, student=None):
    """
    Main method that sends off the report
    """
    SENDERS = {
        "email": send_email,
        "file": send_file
    }

    send_method = report["send_method"]
    SENDERS[send_method](report, report_text, student)

def send_email(report, report_text, student):
    """
    Send the text over the email
    """
    message = email.message_from_string(report_text)
    message['To'] = transform_format_codes(report['destination'], student)
    message['From'] = transform_format_codes(report['source'], student)
    message['Subject'] = transform_format_codes(report['subject'], student)
    #TODO support greater variety of smtp servers types as well as smtps
    with smtplib.SMTP('localhost') as email_server:
        email_server.send_message(message)

def send_file(report, report_text, student):
    """
    Send the text to a file
    """
    destination = transform_format_codes(report['destination'], student)
    with open(destination, 'w') as outfile:
        outfile.write(report_text)


def transform_format_codes(dest, student):
    """
    transform the destination address to use format codes
    """
    if student is None and ("%u" in dest or "%e" in dest):
        raise Exception
    elif student is not None:
        dest = dest.replace('%u', student['username'])
        dest = dest.replace('%e', student['email'])
    date = str(datetime.date.today())
    dest = dest.replace('%d', date)
    return dest

