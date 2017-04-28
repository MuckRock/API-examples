#!/usr/bin/env python2

# A script that will take a CSV of submitted agency tasks and save that data into agencies that have not been approved or had data
# added to them yet.
#
#

import requests
import unicodecsv
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 1

with open('imported_agency_info.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        a = requests.get((url+"agency/"+str(row["Input.Agency"])), headers=headers)
        agency_json = a.json()
        print "We're looking up new agency info for " + agency_json["name"]
        if agency_json['status'] is "pending" and agency_json['phone'] is None and agency_json['email'] is None and agency_json['address'] is None and agency_json['fax'] is None and agency_json['website'] is None# Make sure no one has done the agency in the meantime
            print agency_json["name"] + "<- Agency has not been done yet. Adding info"
            data = json.dumps({
                'address': row["Address"],
                'email': row["Email"]
                'fax': row["Fax"]
                'phone': row["Phone"]
                'website': row["Website"]
            })
            http_request.patch(url+"agency/"+str(row["Input.Agency"]), headers=headers, data=data)
