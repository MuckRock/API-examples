#!/usr/bin/env python2
# -- coding: utf-8 --

import urllib, os, json, datetime, requests, urlparse

# token = '' #If you want to export embargoed requests, you'll need to put in an API token that gives you permissions to them.
# headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'} #Uncomment for token usage.

APIurl = 'https://www.muckrock.com/api_v1/'



headers = {'content-type': 'application/json'} #Uncomment for no token

request_pks = [
                    6996
                ]


for pk in request_pks:
    print "Working on request " + str(pk)
    #print headers
    r = requests.get(APIurl + 'foia/%d/' % pk, headers=headers) 
    json_data = r.json()
    
    a = requests.get(APIurl + 'agency/%d/' % json_data['agency'], headers=headers)
    agency_data = a.json()

    communications = json_data['communications']
	
    if communications is None:
        print "It looks like there were no communications here."
    
    if not os.path.exists(str(pk)): # Checks to see if the folder exists.
        dirName = agency_data['name'] + ' ' + json_data['tracking_id'] + ' ' + json_data['user']
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
            #urllib.urlretrieve(url, '/'+str(pk)+'/'+filename)
            urllib.urlretrieve(url, dirName + '/' + filename)
            
        
        print "Trying to grab the text from the communication"
        # eventually this should save to pdf, maybe using this: https://github.com/mstamy2/PyPDF2/tree/master/Sample_Code
        
        communicationText = communication["communication"].encode('ascii', 'ignore')
        text_file = open(dirName + '/' + communication["date"] + " Communication.txt", "w+")
        text_file.write(communicationText)
        text_file.close()
