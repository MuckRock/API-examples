#!/usr/bin/env python2
# -- coding: utf-8 --

import requests as http_request
import json
import utils
import unicodecsv


unacknowledged_file = open('cialetter_unacknowledged.txt', 'w')
acknowledged_file = open('cialetter_acknowledged.txt', 'w')

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

agencyID = raw_input('AgencyID: ')
next_url = "https://www.muckrock.com/api_v1/foia/?agency=" + agencyID
current_page = 0

while next_url:
    # we use next_url because the API results are paginated
    r = http_request.get(next_url, headers=headers)
    data = r.json()
    next_url = data['next']

    # measures progress by page, not by result
    current_page += 1
    total_pages = (data['count'] / 20.0)
    utils.display_progress(current_page, total_pages)

    for request in data['results']:
        if request['status'] == 'ack':
            # Means Awaitng Ack
            request_id = request['id']

            request_url = 'https://www.muckrock.com/api_v1/foia/%s/' % str(request_id)

            print "Working on request " + str(request_id)

            unacknowledged_file.write("\n" + "\n"+ "Subject Heading: " + str(request['title'].encode('utf-8').strip()) + "\n" + "\n")

            unacknowledged_file.write("Request URL: muckrock.com" + str(request['absolute_url']) + "\n" + "\n")

            unacknowledged_file.write("Summary: "  + str(request['description'].encode('utf-8').strip())[0:300] + "\n" + "\n")

            unacknowledged_file.write("Submitted: " + str(request['date_submitted']) + "\n")


            unacknowledged_file.write("Estimated Completion Date: " + str(request['date_due'])+ "\n")

            unacknowledged_file.write("Last Response From Agency: " + str(request['date_followup'])+ "\n" + "\n")

            unacknowledged_file.write("MuckRock" + "\n")
            unacknowledged_file.write("DEPT MR" + str(request_id))
            unacknowledged_file.write("411A Highland Ave" + "\n" + "Somerville, MA 02144-2516")

        elif request['status'] == 'processed':
            #processed is Awaiting Response
            request_id = request['id']
            request_url = 'https://www.muckrock.com/api_v1/foia/%s/' % str(request_id)


            acknowledged_file.write("\n" + "\n"+ "Subject Heading: " + str(request['title'].encode('utf-8').strip()) + "\n" + "\n")

            acknowledged_file.write("Request URL: muckrock.com" + str(request['absolute_url']) + "\n" + "\n")

            acknowledged_file.write("Summary: "  + str(request['description'].encode('utf-8').strip())[0:300] + "\n" + "\n")

            acknowledged_file.write("Submitted: " + str(request['date_submitted']) + "\n")


            acknowledged_file.write("Estimated Completion Date: " + str(request['date_due'])+ "\n")

            acknowledged_file.write("Last Response From Agency: " + str(request['date_followup'])+ "\n" + "\n")

            acknowledged_file.write("MuckRock" + "\n")
            acknowledged_file.write("DEPT MR" + str(request_id))
            acknowledged_file.write("411A Highland Ave" + "\n" + "Somerville, MA 02144-2516")





        else: #put stuff here
            print "No Match."
