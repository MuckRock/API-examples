#!/usr/bin/env python2

import requests

user = raw_input('Username? ')
pw = raw_input('Password? ')

#r = requests.post('http://localhost:8000/api_v1/token-auth/', data={'username': user, 'password': pw})
r = requests.post('https://www.muckrock.com/api_v1/token-auth/', data={'username': user, 'password': pw})

json = r.json()
if 'token' in json:
    print json['token']
else:
    print json
