#!/usr/bin/env python2

import requests
import unicodecsv
from utils import get_api_key

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'communication'

fields = (
    "id",
    "ffile",
    "title",
    "date",
    "source",
    "description",
    "access",
    "doc_id",
    "pages"
)

page = 1

csv_file = open('doccloudfiles.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(fields)

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            print "datum"
            for docfile in datum['files']:
                print docfile
                csv_writer.writerow([docfile[field] for field in fields])
                print "docfile"
        print 'Page %d of %d' % (page, json['count'] / 20 + 1)
        page += 1
    except Exception as e:
        print e
