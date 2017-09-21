#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import unicodecsv
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

next_ = url + 'responsetask'

fields = (
    'id',
    'resolved_by',
    'communication',
    'date_created',
    'date_done',
    'resolved',
    'created_from_orphan',
    'predicted_status',
    'predicted_status',
)

page = 1

csv_file = open('tasks.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(fields)

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            csv_writer.writerow([datum[field] for field in fields])
        print 'Page %d of %d' % (page, json['count'] / 20 + 1)
        page += 1
    except:
        print r
        print r.text
