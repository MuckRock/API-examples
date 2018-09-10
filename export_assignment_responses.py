#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import unicodecsv
from utils import get_api_key

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}


assignmentID = raw_input('What assignment are you trying to export? Look at the numbers at the end of the URL:  ')
next_ = url + "assignment-responses/?crowdsource=" + str(assignmentID)

basic_fields = [
"id",
"user",
"datetime",
"tags",
"skip",
"number",
"flag",
"gallery",
"crowdsource"
]

assignment_fields = []

page = 1

csv_file = open('assignment ' + str(assignmentID) +  ' export.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)


r = requests.get(next_, headers=headers)
json = r.json()

for column in json['results'][0]['values']:
    assignment_fields.append(column['field'])
csv_writer.writerow(basic_fields + assignment_fields)

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            submissions = []
            for field in basic_fields:
                submissions.append(datum[field])
            for entry in datum["values"]:
                submissions.append(entry["value"])
            csv_writer.writerow(submissions)
#            csv_writer.writerow(datum[field] for field in basic_fields + )
            # + datum['values'][assignment_fields] for field in assignment_fields
        print 'Page %d of %d' % (page, json['count'] / 40)
        page += 1
    except Exception as e:
        print e
