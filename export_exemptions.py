#!/usr/bin/env python2
# -- coding: utf-8 --

import utils
import urllib, os, json, datetime, requests, urlparse

api_url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 1
next_url = api_url + "exemption/?page=" + str(page)
done_so_far = 0

try:
    os.mkdir('exemptions')
except Exception as e:
    print 'dir exists'

while next_url:
    exemptions = requests.get(next_url , headers=headers).json()
    exemption_data = exemptions['results']
    for exemption in exemption_data:
        text_file = open('exemptions/' + str(exemption["id"]) + ".json", "w+")
        text_file.write(json.dumps(exemption, sort_keys=True, indent=4, separators=(',', ': ')))
        text_file.close()

    done_so_far = done_so_far + len(exemption_data)
    count = exemptions['count']
    print 'Getting exemptions: %d of %d' % (done_so_far, count)
    next_url = exemptions['next']
