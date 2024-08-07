#!/usr/bin/env python2
# -- coding: utf-8 --

import os
import sys
from getpass import getpass

import requests

# Using this method of secret storing:
# https://stackoverflow.com/questions/25501403/storing-the-secrets-passwords-in-a-separate-file

try:
    import credentials
    token = credentials.API_key
except Exception as e:
    print (e)
    token = getpass("API Token: ")
    credentials_file = open("credentials.py", "w")
    credentials_file.writelines("API_key = \"" + token +"\"")
    credentials_file.close


API_URL = 'https://www.muckrock.com/api_v1/'

def get_api_key():
    return token

def get_headers(token=None):
    if token:
        return {
            'Authorization': 'Token %s' % token,
            'content-type': 'application/json'
        }
    else:
        return {'content-type': 'application/json'}

def display_progress(current, total):
    percent = (current / total) * 100.00
    sys.stdout.write("\r%d%%" % percent)
    sys.stdout.flush()
