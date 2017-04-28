#!/usr/bin/env python2

import requests
import unicodecsv
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

next_ = url + 'newagencytask'

task_fields = (
            'id',
            'agency',
            'resolved'
)

agency_fields = (
            'id',
            'name',
            'status',
            'jurisdiction',
            'address',
            'email',
            'other_emails',
            'phone',
            'fax',
            'website'
)

page = 1

csv_file = open('incomplete_agencies.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(task_fields + agency_fields + ("Jurisdiction Name",))

print "OK, set up the file"

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            print "The task " + str(datum["id"]) + " is " + str(datum["resolved"])
            if not (datum["resolved"]):
                a = requests.get((url+"agency/"+str(datum["agency"])), headers=headers)
                agency_json = a.json()
                print "We're looking up new agency info for " + agency_json["name"]
                all_fields = dict(datum)
                all_fields.update(agency_json)
                print "Created all fields. whatever the hell that is"
                print "Looking up jurisdiction " + str(agency_json["jurisdiction"])
                print url+"jurisdiction/"+str(agency_json["jurisdiction"])
                j = requests.get((url+"jurisdiction/"+str(agency_json["jurisdiction"])), headers=headers)
                jurisdiction_json = j.json()
                if jurisdiction_json["full_name"] is True:
                    jurisdiction2 = jurisdiction_json["full_name"]
                    print "The jurisdiction's full name is " + jurisdiction2
                else:
                    jurisdiction2 = jurisdiction_json["name"]
                    print "The jurisdiction is a state and its full name is " + jurisdiction2
                all_fields.update({'jurisdiction2': jurisdiction2})
                print all_fields
                csv_writer.writerow(all_fields[field] for field in task_fields+agency_fields+ ("jurisdiction2",))
        print 'Page %d of %d' % (page, json['count'] / 20 + 1)
        page += 1
    except:
        print "OMG!!!!"
        #print r
        #print r.text
