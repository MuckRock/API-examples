#!/usr/bin/env python2

import requests
import unicodecsv
from utils import get_api_key

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'agency'

fields = (
"id",
"name",
"slug",
"status",
"twitter",
"twitter_handles",
"parent",
"appeal_agency",
"url",
"foia_logs",
"foia_guide",
"public_notes",
"absolute_url",
"average_response_time",
"fee_rate",
"success_rate",
"has_portal",
"has_email",
"has_fax",
"has_address",
"number_requests",
"number_requests_completed",
"number_requests_rejected",
"number_requests_no_docs",
"number_requests_ack",
"number_requests_resp",
"number_requests_fix",
"number_requests_appeal",
"number_requests_pay",
"number_requests_partial",
"number_requests_lawsuit",
"number_requests_withdrawn"
)

page = 1

csv_file = open('agency_stats.csv', 'w')
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
    except Exception as e:
        print e
