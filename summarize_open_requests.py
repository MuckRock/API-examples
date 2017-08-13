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
    unacknowledged_file.write("Below are requests that we have no record of ever being acknowledged. We have included the first 200 characters of the request, as well as subject heading, for help in identifying the request.\n\n\n")
    acknowledged_file.write("Below are requests that were acknolwedged but we have not yet recevied a final response for. We have included the first 200 characters of the request, as well as subject heading, for help in identifying the request. \n\n\n")


    for request in data['results']:
        if request['status'] == 'ack':
            # Means Awaitng Ack
            request_id = request['id']
            request_url = 'https://www.muckrock.com/api_v1/foia/%s/' % str(request_id)

            print "Working on request " + str(request_id)


            unacknowledged_file.write("\n" + "\n"+ "Subject Heading: " + str(request['title'].encode('utf-8').strip()) + "\n" + "\n")
            if request['embargo'] is False:
                unacknowledged_file.write("Request URL: muckrock.com" + str(request['absolute_url']) + "\n" + "\n")
            unacknowledged_file.write("Summary: "  + str(request['description'].encode('utf-8').strip())[0:300] + "\n" + "\n")
            unacknowledged_file.write("Submitted: " + str(request['date_submitted']) + "\n")
            if request['communications'][0]["from_who"]:
                print "Got a requester's name! It's " + request['communications'][0]["from_who"]
                unacknowledged_file.write("Requester Name: " + request['communications'][0]["from_who"] + "\n")
            else:
                    print "No requester's name"
            unacknowledged_file.write("MuckRock" + "\n")
            unacknowledged_file.write("DEPT MR" + str(request_id))
            unacknowledged_file.write("411A Highland Ave" + "\n" + "Somerville, MA 02144-2516")
            unacknowledged_file.write("\n\n\n================================\n================================\n================================\n")
            unacknowledged_file.write("Address associated with this request:\n\n MuckRock \n")


        elif request['status'] == 'processed':
            #processed is Awaiting Response
            request_id = request['id']
            request_url = 'https://www.muckrock.com/api_v1/foia/%s/' % str(request_id)
            acknowledged_file.write("\n" + "\n"+ "Subject Heading: " + str(request['title'].encode('utf-8').strip()) + "\n" + "\n")

            if request['embargo'] is False:
                acknowledged_file.write("Request URL: muckrock.com" + str(request['absolute_url']) + "\n" + "\n")
            acknowledged_file.write("Summary: "  + str(request['description'].encode('utf-8').strip())[0:300] + "\n" + "\n")
            acknowledged_file.write("Submitted: " + str(request['date_submitted']) + "\n")

            if request['communications'][0]["from_who"]:
                print "Got a requester's name! It's " + request['communications'][0]["from_who"]
                acknowledged_file.write("Requester Name: " + request['communications'][0]["from_who"] + "\n")
            else:
                print "No requesters name"
            if request['date_due'] is not None:
                acknowledged_file.write("Estimated Completion Date: " + str(request['date_due'])+ "\n\n")
            else:
                acknowledged_file.write("Estimated Completion Date: We have not received an estimated completion date for this request.\n\n")
            if request['tracking_id'] is not None:
                acknowledged_file.write("Tracking Number: " + str(request['tracking_id'])+ "\n\n")
            else:
                acknowledged_file.write("Tracking Number: We have not received a tracking number for this request.\n\n")
            acknowledged_file.write("Last Response From Agency: " + str(request['date_followup'])+ "\n" + "\n")

            acknowledged_file.write("Address associated with this request:\n\nMuckRock \n")
            acknowledged_file.write("DEPT MR" + str(request_id))
            acknowledged_file.write("\n411A Highland Ave\nSomerville, MA 02144-2516")
            acknowledged_file.write("\n\n\n================================\n================================\n================================\n")

        else: #put stuff here
            print "No Match."
