#!/usr/bin/env python2
# -- coding: utf-8 --

import utils
import urllib, os, json, datetime, requests, urlparse

api_url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 1
next_url = api_url + "jurisdiction/?page=" + str(page)
done_so_far = 0

try:
    os.mkdir('jurisdictions')
except Exception as e:
    print 'dir exists'

while next_url:
    jurisdictions = requests.get(next_url , headers=headers).json()
    jurisdiction_data = jurisdictions['results']
    for jurisdiction in jurisdiction_data:
        text_file = open('jurisdictions/' + str(jurisdiction["id"]) + ".json", "w+")
        text_file.write(json.dumps(jurisdiction, sort_keys=True, indent=4, separators=(',', ': ')))
        text_file.close()

    done_so_far = done_so_far + len(jurisdiction_data)
    count = jurisdictions['count']
    print 'Getting jurisdictions: %d of %d' % (done_so_far, count)
    next_url = jurisdictions['next']
