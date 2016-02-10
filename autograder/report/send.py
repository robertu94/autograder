#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for reporting student results in several different
formats.
"""
import smtplib
import email
import datetime

def send_email(settings, report_id, report_text):
    """
    Send the text over the email
    """
    message = email.message_from_string(report_text)
    message['To'] = transform_format_codes(settings['reports'][report_id]['destination'])
    message['From'] = transform_format_codes(settings['reports'][report_id]['source'])
    message['Subject'] = transform_format_codes(settings['reports'][report_id]['subject'])
    #TODO support greater variety of smtp servers types as well as smtps
    with smtplib.SMTP('localhost') as email_server:
        email_server.send_message(message)

def send_to_file(settings, report_id, report_text):
    """
    Send the text to a file
    """
    destination = transform_format_codes(settings['reports'][report_id]['destination'])
    with open(destination, 'w') as outfile:
        outfile.write(report_text)


def transform_format_codes(dest):
    """
    transform the destination address to use format codes
    """
    user_username = "user"
    user_email = "email"
    date = str(datetime.date.today())
    dest = dest.replace('%u', user_username)
    dest = dest.replace('%e', user_email)
    dest = dest.replace('%d', date)
    return dest

