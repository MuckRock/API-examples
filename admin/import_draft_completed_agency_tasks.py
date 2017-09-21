#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import unicodecsv
import utils
import json


url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 1

with open('agency_upload.csv') as csvfile:
    reader = unicodecsv.DictReader(csvfile)
    for row in reader:
        try:
            agency_url = url+"agency/"+str(row["Input.agency"])+"/"
            print agency_url
            a = requests.get(agency_url, headers=headers)
            agency_json = a.json()
            print "We're looking up new agency info for " + agency_json["name"]
            if agency_json['status'] == "pending" and agency_json['phone'] == '' and agency_json['email'] == '' and agency_json['address'] == '' and agency_json['fax'] == '' and agency_json['website'] == '':# Make sure no one has done the agency in the meantime
                print "Doing the R thang"
                r = requests.get(agency_url, headers=headers)
                data = json.dumps({
                    'address': row["Answer.address"],
                    'email': row["Answer.email"],
                    'fax': row["Answer.fax"],
                    'phone': row["Answer.phone"],
                    'website': row["Answer.website"]
                })
                print agency_url
                requests.patch(agency_url, headers=headers, data=data)
            else:
                print "That agency has already been tweaked"
        except:
            print "Error with agency " + row["Input.agency"] + ", usually because it was deleted."
