#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import json
import csv

# Step 1: Create a file "file_with_agencies.csv" and add the agency IDs you want to file with in it, one per line. You can use 248 and 21983 as test agencies. You do not normally need to modify the following line. Filing with test agencies will deduct requests from your account, but if you reach out we can refund those requests or you can cancel them yourself within 30 minutes.


# Step 2: Create a file "requestLanguage.txt" with the text of the request. This should be the full length of the request and include any salutations. Do not include contact information — MuckRock generates this on a per request basis. Update the below with your request's title as indicated

f = open("requestLanguage.txt","r")

# Step 3: When possible, we recommend avoiding adding attachments as agencies receive requests in a variety of ways. If needed, you can define a file to attach here. Uncomment this line, update the attachment name as appropriate, and then uncomment out the line beginning ""# 'attachments':" below as well.

# attachment = "file.pdf"

# Step 3: Check your API key from your profile page, located lower left of the page here: https://www.muckrock.com/accounts/profile/ Put that API key below, as indicated:

token = "1234"

# Be careful: Anyone with access to your API key has full access to your account!

# Step 4: Uncomment embargo settings ("'embargo': True") as appropriate. Using embargo is dependent on your plan type on MuckRock.

# Step 5: Execute command, python2 bulk_file.py


with open('file_with_agencies.csv', 'rt') as f:
    reader = csv.reader(f)
    agencies = list(reader)

url = 'https://www.muckrock.com/api_v1/'
headers = {
        'Authorization': 'Token %s' % token,
        'content-type': 'application/json'
    }

print("About to file this request .... /n")
f = open("requestLanguage.txt","rt")
message = f.read()

print(message)

for agency in agencies:

    # Sample Structure: https://www.muckrock.com/api_v1/agency/100/
    agency_url = url + 'agency/' + str(agency[0]) + '/'
    print(agency_url)
    a = requests.get(agency_url, headers=headers)
    agency_name = a.json()['name']
    title = agency_name + " Request" # Update this with title
    data = json.dumps({
        'agency': agency,
        'title': title,
        'full_text': message,
#        'attachments': [attachment],
#         'embargo': True
        'permanent_embargo': True
        })

    # The request will be saved as a draft if you do not have any requests left
    r = requests.post(url + 'foia/', headers=headers, data=data)
    print(r)
    print("If it says 201, succesfully filed with " + agency_name)
    # 402 errors indicate that your request did not have enouhg requests to file, and saved it as a draft.
    # You may need to log in to MuckRock and switch the active organization to make sure you're drawing from the correct pool.
