#!/usr/bin/env python2
# -- coding: utf-8 --

# Standard Library
import datetime
import json
import os
import time

# Third Party
import requests
from simplejson.scanner import JSONDecodeError

import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 599
next_ = url + 'foia/?embargo=3&page=%d' % page

agencies = {}
jurisdictions = {}

def get_jurisdiction(jurisdiction_id):
    global jurisdictions
    if jurisdiction_id in jurisdictions:
        return jurisdictions[jurisdiction_id]
    else:
        print 'getting jurisdiction', jurisdiction_id
        r = requests.get(url + 'jurisdiction/' + str(jurisdiction_id), headers=headers)
        jurisdiction_json = r.json()
        jurisdiction = '%s_%s' % (jurisdiction_id, jurisdiction_json['slug'])
        jurisdictions[jurisdiction_id] = jurisdiction
        return jurisdiction


while next_ is not None: # Handling at the page level
    try:
        r = requests.get(next_, headers=headers)
        json_data = r.json()
        print 'Page %d of %d (%d total)' % (page, json_data['count'] / 50 + 1, json_data['count'])
        page += 1
        next_ = json_data['next']
        print next_
        for request in json_data['results']:
            print 'Working on request ' + str(request['id'])

            if request['status'] == 'started':
                continue

            if request['agency'] in agencies:
                agency, jurisdiction = agencies[request['agency']]
            else:
                if request['agency'] is None:
                    agency = 'None'
                    jurisdiction = 'None'
                else:
                    print 'getting agency', request['agency']
                    r = requests.get(url + 'agency/' + str(request['agency']), headers=headers)
                    agency_json = r.json()
                    agency = '%s_%s' % (request['agency'], agency_json['slug'])
                    jurisdiction = get_jurisdiction(agency_json['jurisdiction'])
                    agencies[request['agency']] = (agency, jurisdiction)

            communications = request['communications']

            dir_name = '%s/%s/%s_%s' % (jurisdiction, agency, request['id'], request['slug'])
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            for i, communication in enumerate(communications):
                for file_ in communication['files']:
                    fileurl = file_['ffile']
                    file_name = '%s_%s' % (file_['datetime'], fileurl.split('/')[-1])
                    file_name = '%s/%s' % (dir_name, file_name)
                    if not os.path.exists(file_name):
                        with open(file_name, 'wb') as f:
                            f.write(requests.get(fileurl).content)

                communication_text = communication['communication'].encode('ascii', 'ignore')
                date = communication['datetime'].split('T')[0]
                with open('%s/%s_%s_communication.txt' % (dir_name, date, i), 'w') as f:
                    f.write(communication_text)

    except JSONDecodeError:
        print r.status_code
        print r.content
        raise
    except KeyboardInterrupt:
        import ipdb
        ipdb.set_trace()

