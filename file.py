#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import json
import utils

import csv

with open('agencies.csv', 'rb') as f:
    reader = csv.reader(f)
    agencies = list(reader)

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

f = open("requestLanguage.txt","r")
message = f.read()

print message # Just to help verify that the language is what you want included.

# If you'd like to file a test request, test agency is 248. Note that this uses a request, which you can ask and we'll refund.

for agency in agencies:
    print "Filing with " + str(agency)
    data = json.dumps({
        'agency': agency,
        'title': 'My Public Records Request',
        'full_text': message, # Use if you don't want any MuckRock preamble/post-amble text added.
#        'document_request': message, # use if you do want template added around your message text
#        'attachments': ['https://muckrock.s3.us-east-1.amazonaws.com/files_static/some_attachment.pdf'],
        'permanent_embargo': True
#        'embargo': True
        })
    # The request will be saved as a draft if you do not have any requests left
    r = requests.post(url + 'foia/', headers=headers, data=data)
    print(r)
