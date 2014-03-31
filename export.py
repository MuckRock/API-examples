#!/usr/bin/env python2
# -- coding: utf-8 --

import urllib, os, json, datetime, requests, urlparse

token = '' #If you want to export embargoed requests, you'll need to put in an API token that gives you permissions to them.
url = 'https://www.muckrock.com/api_v1/'

# Stuff borrowed from http://stackoverflow.com/questions/6373094/how-to-download-a-file-to-a-specific-path-in-the-server-python

if token:
    headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}
else:
    headers = {'content-type': 'application/json'}

request_pks = [10565]

for pk in request_pks:
    print "Working on request " + str(pk)
    r = requests.get(url + 'foia/%d/' % pk, headers=headers)
    json_data = r.json()
    communications = json_data['communications']
	
    if communications is None:
        print "It looks like there were no communications here."
    
    if not os.path.exists(str(pk)): # Checks to see if the folder exists.
        dirName = str(pk)
        print "Creating directory /" + str(pk)
        os.makedirs(str(pk))
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
            print filename
            #urllib.urlretrieve(url, '/'+str(pk)+'/'+filename)
            urllib.urlretrieve(url, str(pk) + '/' + filename)
            
        
        print "Trying to grab the text from the communication"
        # eventually this should save to pdf, maybe using this: https://github.com/mstamy2/PyPDF2/tree/master/Sample_Code
        
        communicationText = communication["communication"].encode('ascii', 'ignore')
        text_file = open(str(pk) + '/' + communication["date"] + " Communication.txt", "w+")
        text_file.write(communicationText)
        text_file.close()
