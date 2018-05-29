#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import unicodecsv
from utils import get_api_key
from datetime import datetime


token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'news'

fields = (
"pub_date",
"title",
"kicker",
"slug",
"summary",
"body",
"publish",
"image"
)

page = 1

keyword = raw_input('What key word or string do you want to check for? ')


csv_file = open('news_links.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(fields, "url")

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            if keyword in datum["body"]:
                pub_date_object = datetime.strptime(datum["pub_date"])
#                csv_writer.writerow([datum[field] for field in fields])
                csv_writer.writerow("https://www.muckrock.com/news/archives/" + str(pub_date_object.strftime(%Y)) +
                "/" + str(pub_date_object.strftime(%b).lower()) + "/" + str(pub_date_object.strftime(%d)) + "/" + datum["slug"])
        print 'Page %d of %d' % (page, json['count'] / 20 + 1)
        page += 1
    except Exception as e:
        print e
