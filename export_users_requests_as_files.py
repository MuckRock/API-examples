#!/usr/bin/env python2
# -- coding: utf-8 --

import urllib, os, json, datetime, requests, urlparse
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)


user = raw_input('Username to export (case sensitive):')
# user = "USERNAME" #<--- Put username here. Case sensitive.

page = 1
next_ = url+"foia/?user="+user


# still need to find a nice way to specify pks from console
# request_pks = [6996]


while next_ is not None:
    print "URL I'm using is " + next_
    r = requests.get(next_, headers=headers)

    print "hey rob. check out " + str(r)
    try:
        json_data = r.json()
        print 'Page %d of %d' % (page, json_data['count'] / 20 + 1)
        next_ = json_data['next']
        for request in json_data['results']:
            print "Working on request " + str(request["id"])
            # get request first

            request_url = url + 'foia/%d/' % request["id"]
#            request = requests.get(request["url"], headers=headers) #original
            r = requests.get(request_url, headers=headers) #original

            request_data = r.json()
            # get agency second

            print "Here is the agency number " + str(request["agency"])
            agency = requests.get("https://www.muckrock.com/api_v1/agency/" + str(request["agency"]), headers=headers)

            agency_data = agency.json()
            # get communications third

            communications = request['communications']

            if communications is None:
                print "No communications for request #%d." % request["id"]
            print "before"

            if not os.path.exists(str(request["id"])): # Checks to see if the folder exists.
                username = requests.get(url + 'user/%d/' % request['user'], headers=headers).json()['username']
                print username
                dirName = username + '_' + agency_data['name'] + '_' + request_data['tracking_id']
                # TODO better sanitization on directory names
                print "Creating directory " + dirName
                dirName = dirName.replace(";", "") # to sanitize it from semi-colons
                dirName = dirName.replace(":", "") # to sanitize it from colons
                os.makedirs(dirName)
            else:
                print "The directory already exists. Phew."
            print "after"

            for communication in communications:
                commNum = 0
                #print communication
                for file in communication['files']:
                    print "Trying to grab a file from communication " + str(commNum)
                    url = file['ffile']
                    split = urlparse.urlsplit(url) # grabbed from http://stackoverflow.com/questions/2795331/python-download-without-supplying-a-filename
                    filename = split.path.split("/")[-1]
                    filename = str(communication["date"])+" "+filename
                    filename = filename.replace(";", "") # to sanitize it from semi-colons
                    filename = filename.replace(":", "") # to sanitize it from colons
                    print filename
                    #urllib.urlretrieve(url, '/'+str(request_id)+'/'+filename)
                    urllib.urlretrieve(url, dirName + '/' + filename)


                print "Trying to grab the text from the communication"
                # eventually this should save to pdf, maybe using this: https://github.com/mstamy2/PyPDF2/tree/master/Sample_Code

                communicationText = communication["communication"].encode('ascii', 'ignore')
                text_file = open(dirName + '/' + communication["date"] + " Communication.txt", "w+")
                text_file.write(communicationText)
                text_file.close()
    except:
      print "There was an error of unkown origin"
#        print r
#        print r.text
