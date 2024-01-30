#!/usr/bin/env python2
# -- coding: utf-8 --

import datetime
import json
import os
import time
import urllib
import urlparse

import requests

import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)


user = raw_input('Username to export (case sensitive):')
# user = "USERNAME" #<--- Put username here. Case sensitive.
# request_pks = [6996] #<--- To export by MR number

page = 1
next_ = url+"foia/?user="+user




while next_ is not None: # Handling at the page level
    resp = requests.get(next_, headers=headers)
    try:
        json_data = resp.json()
        print "\n" + ("*" * 100)
        print 'Page %d of %d' % (page, json_data['count'] / 50 + 1)
        print ("*" * 100) + "\n"
        page += 1
        next_ = json_data['next']
        for request in json_data['results']:
            time.sleep(3)
            print "\nWorking on request " + str(request["id"])
            request_url = url + 'foia/%d/' % request["id"]
            resp = requests.get(request_url, headers=headers) #original

            request_data = resp.json()

            print "Here is the agency number " + str(request_data["agency"])
            resp = requests.get("https://www.muckrock.com/api_v1/agency/" + str(request_data["agency"]), headers=headers)

            agency_data = resp.json()
            # get communications third

            communications = request_data['communications']

            if communications is None:
                print "No communications for request #%d." % request_data["id"]

            resp = requests.get(url + 'user/%d/' % request_data['user'], headers=headers)
            username = resp.json()['username']
            print username
            dirName = username + '_' + agency_data['name'] + '_' + str(request_data['id'])
            if not os.path.exists(dirName): # Checks to see if the folder exists.
                # TODO better sanitization on directory names
                print "Creating directory " + dirName
                dirName = dirName.replace(";", "") # to sanitize it from semi-colons
                dirName = dirName.replace(":", "") # to sanitize it from colons
                os.makedirs(dirName)
            else:
                print "The directory already exists. Phew.", dirName

            with open(dirName + "/agency.txt", "w") as agency_file:
                for email in agency_data["emails"]:
                    if email["request_type"] == "primary" and email["email_type"] == "to":
                        agency_file.write(email["email"]["email"] + "\n\n")
                        break
                for addr in agency_data["addresses"]:
                    if addr["request_type"] == "primary":
                        agency_file.write("%(street)s, %(city)s %(state)s %(zip_code)s\n\n" % addr["address"])
                        break

            for communication in communications:
                #print communication
                for file in communication['files']:
                    fileurl = file['ffile']
                    split = urlparse.urlsplit(fileurl) # grabbed from http://stackoverflow.com/questions/2795331/python-download-without-supplying-a-filename
                    filename = split.path.split("/")[-1]
                    filename = str(communication["datetime"])+" "+filename
                    filename = filename.replace(";", "") # to sanitize it from semi-colons
                    filename = filename.replace(":", "") # to sanitize it from colons
                    urllib.urlretrieve(fileurl, dirName + '/' + filename)


                print "Trying to grab the text from the communication"
                # eventually this should save to pdf, maybe using this: https://github.com/mstamy2/PyPDF2/tree/master/Sample_Code

                communicationText = communication["communication"].encode('ascii', 'ignore')
                text_file = open(dirName + '/' + communication["datetime"] + " Communication.txt", "w+")
                text_file.write(communicationText)
                text_file.close()
                print "File closed"

    except Exception as exc:
      print "There was an error of unkown origin"
      print(resp.content)
      raise
