#!/usr/bin/env python2
# -- coding: utf-8 --

import urllib, os, json, datetime, requests, urlparse
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
    r = requests.get(next_, headers=headers)
    try:
        json_data = r.json()
        print 'Page %d of %d' % (page, json_data['count'] / 20 + 1)
        next_ = json_data['next']
        for request in json_data['results']:
            print "Working on request " + str(request["id"])
            request_url = url + 'foia/%d/' % request["id"]
            r2 = requests.get(request_url, headers=headers) #original

            request_data = r2.json()

            print "Here is the agency number " + str(request_data["agency"])
            agency = requests.get("https://www.muckrock.com/api_v1/agency/" + str(request_data["agency"]), headers=headers)

            agency_data = agency.json()
            # get communications third

            communications = request_data['communications']

            if communications is None:
                print "No communications for request #%d." % request_data["id"]

            if not os.path.exists(str(request_data["id"])): # Checks to see if the folder exists.
                username = requests.get(url + 'user/%d/' % request_data['user'], headers=headers).json()['username']
                print username
                dirName = username + '_' + agency_data['name'] + '_' + request_data['tracking_id']
                # TODO better sanitization on directory names
                print "Creating directory " + dirName
                dirName = dirName.replace(";", "") # to sanitize it from semi-colons
                dirName = dirName.replace(":", "") # to sanitize it from colons
                os.makedirs(dirName)
            else:
                print "The directory already exists. Phew."

            for communication in communications:
                #print communication
                for file in communication['files']:
                    fileurl = file['ffile']
                    split = urlparse.urlsplit(fileurl) # grabbed from http://stackoverflow.com/questions/2795331/python-download-without-supplying-a-filename
                    filename = split.path.split("/")[-1]
                    filename = str(communication["date"])+" "+filename
                    filename = filename.replace(";", "") # to sanitize it from semi-colons
                    filename = filename.replace(":", "") # to sanitize it from colons
                    urllib.urlretrieve(fileurl, dirName + '/' + filename)


                print "Trying to grab the text from the communication"
                # eventually this should save to pdf, maybe using this: https://github.com/mstamy2/PyPDF2/tree/master/Sample_Code

                communicationText = communication["communication"].encode('ascii', 'ignore')
                text_file = open(dirName + '/' + communication["date"] + " Communication.txt", "w+")
                text_file.write(communicationText)
                text_file.close()
                print "File closed"

    except:
      print "There was an error of unkown origin"
#        print r
#        print r.text
