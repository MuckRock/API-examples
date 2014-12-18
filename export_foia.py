#!/usr/bin/env python2

import requests
import unicodecsv

token = ''
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'foia'

fields = ('id', 'user', 'title', 'slug', 'status', 'jurisdiction',
          'agency', 'date_submitted', 'date_done', 'date_due', 'days_until_due',
          'date_followup', 'embargo', 'date_embargo', 'price', 'description',
          'tracking_id', 'tags')

page = 1

with open('foia.csv', 'w') as csv_file:
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
