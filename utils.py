#!/usr/bin/env python2

import requests

def get_api_key():
    user = raw_input('Username? ')
    pw = raw_input('Password? ')

    r = requests.post('https://www.muckrock.com/api_v1/token-auth/', data={'username': user, 'password': pw})

    json = r.json()
    if 'token' in json:
        return json['token']
    else:
        return None
