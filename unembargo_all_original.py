#!/usr/bin/env python2
# -- coding: utf-8 --
import requests
import json
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

user = "NYWFOIL" #<--- Put username here. Case sensitive.

page = 1
next_ = url+"foia/?user="+user



while next_ is not None:
    print "URL I'm using is " + next_
    r = requests.get(next_, headers=headers)
    print "hey rob. check out " + str(r)
    try:
        print "Getting that sweet JSON"
        json_data = r.json()
        print 'Page %d of %d' % (page, json_data['count'] / 20 + 1)
        next_ = json_data['next']
        for request in json_data['results']:
            reqNumber = request["id"]
            editedRequest = requests.get(url + 'foia/%s/' % str(reqNumber), headers=headers)
            print "Embargoing request number " + str(reqNumber) + " for " + request["title"] + " filed by " + request["username"]

            data = json.dumps({
               'embargo': False,
               'date_embargo': None, #Removes the embargo date to make sure it actually embargos.
            })
            editedRequest = requests.patch(url + 'foia/%d/' % reqNumber, headers=headers, data=data)

            print "Request Embargoed."
            if editedRequest.status_code != 200:
                print '*In Ron Burgendy Voice:* Error? ', editedRequest.status_code, r.text
        page += 1
    except Exception as e:
        print e
        print 'Error! ', editedRequest.status_code, ": ", editedRequest.text