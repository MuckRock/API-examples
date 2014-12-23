#!/usr/bin/env python2
# -- coding: utf-8 --
import requests
import json

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'

if token:
    headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
else:
    headers = {'content-type': 'application/json'}


user = "morisy" #<--- Put username here. Case sensitive.

page = 1
next_ = url+"foia/?user="+user



while next_ is not None:
    r = requests.get(next_, headers=headers)
    try:
        json_data = r.json()
        print 'Page %d of %d' % (page, json_data['count'] / 20 + 1)

        next_ = json_data['next']
        for request in json_data['results']:
            reqNumber = request["id"]
            editedRequest = requests.get(url + 'foia/%s/' % str(reqNumber), headers=headers)
            print "Embargoing request number " + str(reqNumber) + " for " + request["title"] + " filed by " + request["username"]

            data = json.dumps({
               'embargo': True,
               'date_embargo': None, #Removes the embargo date to make sure it actually embargos.
            })
            editedRequest = requests.patch(url + 'foia/%d/' % reqNumber, headers=headers, data=data)

            print "Request Embargoed."
            if editedRequest.status_code != 200:
                print '*In Ron Burgendy Voice:* Error? ', editedRequest.status_code, r.text
        page += 1
    except Exception as e:
        print e
        print 'Error! ', editedRequest.status_code, ": ", editdReqeust.text
