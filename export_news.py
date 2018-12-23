#!/usr/bin/env python2
# -- coding: utf-8 --

## Need to install google-api-python-clientself.
## pip install --upgrade google-api-python-client

import requests
import unicodecsv
from utils import get_api_key
from dateutil import parser

# GA_product = raw_input('What is your Google Analytics product Key? ')


token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'news'

fields = (
"id",
"authors",
"editors",
"pub_date",
"title",
"kicker",
"slug",
"summary",
"body",
"publish",
"image"
)

field_names = (
"id",
"authors",
"editors",
"pub_date",
"title",
"kicker",
"slug",
"summary",
"body",
"publish",
"image",
"wordcount",
"title_wordcount",
"full_url"
)

page = 1

csv_file = open('news.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(field_names)

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            pack = [datum[field] for field in fields]
            datum['wordcount'] = len(datum['body'].split())
            datum['title_wordcount'] = len(datum['title'].split())
            datum['full_url'] = 'https://www.muckrock.com/news/archives/' + parser.parse(datum['pub_date']).strftime('%Y') + '/' + parser.parse(datum['pub_date']).strftime('%b').lower() + '/' + parser.parse(datum['pub_date']).strftime('%d') + '/' + datum['slug'] + '/'
            print datum['full_url']
            csv_writer.writerow([datum[field] for field in field_names])
        print 'Page %d of %d' % (page, (json['count'] / 50) + 1)
        page += 1
    except Exception as e:
        print e
