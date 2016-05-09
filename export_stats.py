#!/usr/bin/env python2

# gotta install requests and unicodecsv with pip!
import requests
import unicodecsv
# we provide the utils
import utils

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

if __name__ == '__main__':
    # Gets all the data we need to send a request to the MuckRock API
    token = utils.get_api_key()
    url = utils.API_URL + 'statistics'
    headers = utils.get_headers(token)
    # Opens the stats.csv file and moves us to the beginning to overwrite
    csv_file = open('stats.csv', 'w')
    csv_file.seek(0)
    # Initializes the CSV writer and writes the header row of the CSV
    csv_writer = unicodecsv.writer(csv_file)
    csv_writer.writerow(fields)
    # Gets all the stats and returns them as a single blob of de-paginated data
    stats = utils.get(url, headers)
    # Loops through each stat and writes it as a row in the CSV
    csv_writer.writerow([[stat[field] for field in fields] for stat in stats])
