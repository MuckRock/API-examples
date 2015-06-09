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
"daily_requests_beta",
"daily_articles",
"total_tasks",
"total_unresolved_tasks",
"total_generic_tasks",
"total_unresolved_generic_tasks",
"total_orphan_tasks",
"total_unresolved_orphan_tasks",
"total_snailmail_tasks",
"total_unresolved_snailmail_tasks",
"total_rejected_tasks",
"total_unresolved_rejected_tasks",
"total_staleagency_tasks",
"total_unresolved_staleagency_tasks",
"total_flagged_tasks",
"total_unresolved_flagged_tasks",
"total_newagency_tasks",
"total_unresolved_newagency_tasks",
"total_response_tasks",
"total_unresolved_response_tasks",
"total_faxfail_tasks",
"total_unresolved_faxfail_tasks",
"total_payment_tasks",
"total_unresolved_payment_tasks",
"total_crowdfundpayment_tasks",
"total_unresolved_crowdfundpayment_tasks"
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
