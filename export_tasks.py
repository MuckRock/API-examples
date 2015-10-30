#!/usr/bin/env python2

import requests
import unicodecsv
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

next_ = url + 'task'

fields = (
    'id',
    'date_created',
    'date_done',
    'resolved',
    'assigned',
    'orphantask',
    'snailmailtask',
    'rejectedemailtask',
    'staleagencytask',
    'flaggedtask',
    'newagencytask',
    'responsetask',
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
