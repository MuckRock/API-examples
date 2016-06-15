#!/usr/bin/env python2

import os
import sys
import requests
from getpass import getpass

# Provides the base url as an importable variable
API_URL = 'https://www.muckrock.com/api_v1/'

def get_api_key():
    # try getting an environment variable before requesting the auth information
    try:
        token = os.environ['MUCKROCK_TOKEN']
    except KeyError:
        user = raw_input('Username: ')
        pw = getpass()
        response = requests.post('https://www.muckrock.com/api_v1/token-auth/', data={'username': user, 'password': pw})
        if not response.raise_for_status():
            data = response.json()
            token = data['token']
            os.environ['MUCKROCK_TOKEN'] = token
            print '\nYour token is: %(token)s\n\nSet it for future scripts with this command:\n\nexport MUCKROCK_TOKEN="%(token)s"\n' % {
                'token': token
            }
    return token

def get_headers(token=None):
    if token:
        return {
            'Authorization': 'Token %s' % token,
            'content-type': 'application/json'
        }
    else:
        return {'content-type': 'application/json'}

def get(url, headers):
    """De-paginates the results to a specific URL."""
    response = requests.get(url, headers=headers)
    data = response.json()
    next_page = data['next']
    page_results = data['results']
    if next_page:
        # page results are always a list type, so we combine them with the + operator
        page_results += get(next_page, headers)
    return page_results

def display_progress(current, total):
    percent = (float(current) / total) * 100.00
    sys.stdout.write("\r%d%%" % percent)
    sys.stdout.flush()
