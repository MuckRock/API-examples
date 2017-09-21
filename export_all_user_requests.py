#!/usr/bin/env python2
# -- coding: utf-8 --

import utils
import urllib, os, json, datetime, requests, urlparse


api_url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

username = raw_input('Username: ')
next_url = api_url + "foia/?user=" + username
current_page = 0

while next_url:
    # we use next_url because the API results are paginated
    r = requests.get(next_url, headers=headers)
    data = r.json()
    next_url = data['next']

    # measures progress by page, not by result
    current_page += 1
    total_pages = (data['count'] / 20.0)
    utils.display_progress(current_page, total_pages)

    for result in data['results']:
        request_id = result['id']
        print "Working on request " + str(request_id)
        # get request first
        request_url = api_url + 'foia/%d/' % request_id
        print request_url
        request = requests.get(request_url, headers=headers)
        print request
        request_data = request.json()
        # get agency second
        agency_url = api_url + 'agency/%d/' % request_data['agency']
        agency = requests.get(agency_url , headers=headers)
        agency_data = agency.json()
        # get communications third
        communications = request_data['communications']

        if communications is None:
            print "No communications for request #%d." % request_id

        if not os.path.exists(str(request_id)): # Checks to see if the folder exists.
            username = requests.get(api_url + 'user/%d/' % request_data['user'], headers=headers).json()['username']
            print username
            dirName = username + '_' + agency_data['name'] + '_' + str(request_data['id'])
            # TODO better sanitization on directory names
            print "Creating directory " + dirName
            dirName = dirName.replace(";", "") # to sanitize it from semi-colons
            dirName = dirName.replace(":", "") # to sanitize it from colons
            os.makedirs(dirName)
        else:
            print "The directory already exists. Phew."

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
