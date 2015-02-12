#!/usr/bin/env python2
# -- coding: utf-8 --

import requests as http_request
import json
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

username = raw_input('Username: ')
next_url = url + "foia/?user=" + username
current_page = 0

while next_url:
    # we use next_url because the API results are paginated
    r = http_request.get(next_url, headers=headers)
    data = r.json()
    next_url = data['next']
    
    # measures progress by page, not by result
    current_page += 1
    total_pages = (data['count'] / 20.0)
    utils.display_progress(current_page, total_pages)
    
    for request in data['results']:
        request_id = request['id']
        request_url = 'foia/%s/' % str(request_id)
        # Removes the embargo date to make sure it permanently embargos.
        data = json.dumps({
            'embargo': True,
            'date_embargo': None
        })
        http_request.patch(request_url, headers=headers, data=data)
