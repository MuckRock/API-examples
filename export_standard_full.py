#!/usr/bin/env python2
# -- coding: utf-8 --

import os, json, datetime, requests
import utils, time
from simplejson.scanner import JSONDecodeError

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

page = 476
next_ = url + 'foia/?embargo=3&page=%d' % page

agencies = {}
jurisdictions = {}

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
                agency = agencies[request['agency']]
            else:
                if request['agency'] is None:
                    agency = 'None'
                else:
                    print 'getting agency', request['agency']
                    r = requests.get(url + 'agency/' + str(request['agency']), headers=headers)
                    agency = r.json()
                    agency = '%s_%s' % (request['agency'], agency['slug'])
                    agencies[request['agency']] = agency

            if request['jurisdiction'] in jurisdictions:
                jurisdiction = jurisdictions[request['jurisdiction']]
            else:
                print 'getting jurisdiction', request['jurisdiction']
                r = requests.get(url + 'jurisdiction/' + str(request['jurisdiction']), headers=headers)
                jurisdiction = r.json()
                jurisdiction = '%s_%s' % (request['jurisdiction'], jurisdiction['slug'])
                jurisdictions[request['jurisdiction']] = jurisdiction

            communications = request['communications']

            dir_name = '%s/%s/%s_%s' % (jurisdiction, agency, request['id'], request['slug'])
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            for i, communication in enumerate(communications):
                for file_ in communication['files']:
                    fileurl = file_['ffile']
                    file_name = '%s_%s' % (file_['date'], fileurl.split('/')[-1])
                    with open('%s/%s' % (dir_name, file_name), 'wb') as f:
                        f.write(requests.get(fileurl).content)

                communication_text = communication['communication'].encode('ascii', 'ignore')
                date = communication['date'].split('T')[0]
                with open('%s/%s_%s_communication.txt' % (dir_name, date, i), 'w') as f:
                    f.write(communication_text)

    except JSONDecodeError:
        print r.status_code
        print r.content
        raise
