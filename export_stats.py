#!/usr/bin/env python2

import requests
import unicodecsv
import utils

token = utils.get_api_key()
url = utils.API_URL + 'statistics'
headers = utils.get_headers(token)
next_ = url

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
    "daily_requests_basic",
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

csv_file = open('stats.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(fields)

page = 0
per_page = 50
while next_ is not None:
    response = requests.get(next_, headers=headers)
    data = response.json()
    next_ = data['next']
    total_pages = data['count'] / per_page + 1
    page += 1
    utils.display_progress(page, total_pages)
    for datum in data['results']:
        csv_writer.writerow([datum[field] for field in fields])
print '\n'
