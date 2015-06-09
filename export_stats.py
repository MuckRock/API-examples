#!/usr/bin/env python2

import requests
import unicodecsv
from utils import get_api_key

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
next_ = url + 'statistics'

fields = (
"date",
"total_requests",
"total_requests_success",
"total_requests_denied",
"total_requests_draft",
"total_requests_submitted",
"total_requests_awaiting_ack",
"total_requests_awaiting_response",
"total_requests_awaiting_appeal",
"total_requests_fix_required",
"total_requests_payment_required",
"total_requests_no_docs",
"total_requests_partial",
"total_requests_abandoned",
"total_pages",
"total_users",
"total_agencies",
"total_fees",
"pro_users",
"pro_user_names",
"total_page_views",
"daily_requests_pro",
"daily_requests_community",
"daily_requests_beta"
)

page = 1

csv_file = open('stats.csv', 'w')
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
