#!/usr/bin/env python2

import sys
import requests
from getpass import getpass

API_URL = 'https://www.muckrock.com/api_v1/'

def get_api_key():
    user = raw_input('Username: ')
    pw = getpass()
    request = requests.post('https://www.muckrock.com/api_v1/token-auth/', data={'username': user, 'password': pw})
    json = request.json()
    if 'token' in json:
        return json['token']
    else:
        return None

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

