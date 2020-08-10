#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import unicodecsv
import utils
import datetime

url = utils.API_URL

token = "0cbfdbd42928060646f7a44fd0c04706d02eef1f"

# token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'
headers = utils.get_headers(token)


fields = (
    'id',
    'agency_id',
    'agency',
    'jurisdiction_id',
    'jurisdiction',
    'level',
    'parent',
#    'absolute_url',
    'status',
    'user',
    "embargo",
    "permanent_embargo",
    "datetime_submitted",
    "date_due",
    "days_until_due",
    "date_followup",
    "datetime_done",
    "date_embargo",
    "tracking_id",
    "price",
    "disable_autofollowups",
#    "tags",
    'title'
)

#user = raw_input('Username to export (case sensitive):')
# user = "USERNAME" #<--- Put username here. Case sensitive.
# request_pks = [6996] #<--- To export by MR number

page = 1

# next_ = url+"foia/?user="+user <- use this one if you want to limit to a particular user's requests
# next_ = url+"foia/?page=723"  # <- use this one if you want to start from a page after a crash or failure
next_ = url+"foia/"

page = 1

csv_file = open('foia_data_' + str(datetime.date.today()) + '.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(fields)

while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json = r.json()
        next_ = json['next']
        for datum in json['results']:
            items = []
            print "Working on request with ID " + str(datum['id'])
            for field in fields:
                if field == 'jurisdiction' or field == 'jurisdiction_id' or field == 'level' or field == 'parent' or field == "agency_id":
                    four = 4 # I just need something on this line
                elif field == 'agency':
                    items.append(datum['agency'])
                    agency_url = "https://www.muckrock.com/api_v1/agency/" + str(datum['agency']) + '/'
                    agency = requests.get(agency_url , headers=headers)
                    agency_data = agency.json()
                    agency_name = agency_data['name']
                    items.append(agency_name) ## Things work through here
                    items.append(str(agency_data["jurisdiction"]))
                    jurisdiction_url = "https://www.muckrock.com/api_v1/jurisdiction/" + str(agency_data["jurisdiction"]) + '/'
                    jurisdiction = requests.get(jurisdiction_url , headers=headers)
                    jurisdiction_data = jurisdiction.json()
                    items.append(jurisdiction_data['name']) ## Things work through here
                    items.append(jurisdiction_data['level'])
                    if jurisdiction_data['parent'] != None:
                        if jurisdiction_data['level'] == 's':
                            items.append(jurisdiction_data['name'])
                        else:
                            jurisdiction_url = "https://www.muckrock.com/api_v1/jurisdiction/" + str(jurisdiction_data['parent']) + '/'
                            jurisdiction = requests.get(jurisdiction_url , headers=headers)
                            jurisdiction_data = jurisdiction.json()
                            items.append(jurisdiction_data['name'])
                    else:
                        items.append("United States of America")
                elif field == 'tracking_id':
                    if datum['tracking_id'] == "":
                        items.append("No")
                    else:
                        items.append("Yes")
                else:
                    items.append(datum[field])
            csv_writer.writerow(items)
            time.sleep(1)
        print 'Page %d of %d' % (page, json['count'] / 20 + 1)
        page += 1
    except:
        print r.content
#        print r.text
