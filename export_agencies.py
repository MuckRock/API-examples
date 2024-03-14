#!/usr/bin/env python2
# -- coding: utf-8 --

import utils
import urllib, os, json, datetime, requests, urlparse

api_url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 1
next_url = api_url + "agency/?page=" + str(page)
done_so_far = 0


try:
    os.mkdir('agencies')
except Exception as e:
    print 'dir exists'

while next_url:
    agencies = requests.get(next_url , headers=headers).json()
    agency_data = agencies['results']
    for agency in agency_data:
        text_file = open('agencies/' + str(agency["id"]) + ".json", "w+")
        text_file.write(json.dumps(agency, sort_keys=True, indent=4, separators=(',', ': ')))
        text_file.close()

    done_so_far = done_so_far + len(agency_data)
    count = agencies['count']
    print 'Getting agencies: %d of %d' % (done_so_far, count)
    next_url = agencies['next']
