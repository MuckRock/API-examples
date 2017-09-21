#!/usr/bin/env python2
# -- coding: utf-8 --

import requests
import unicodecsv
from utils import get_api_key

from documentcloud import DocumentCloud
client = DocumentCloud()

client = DocumentCloud(USERNAME, PASSWORD)

# request_pks = ["296716-request-denied"]

csv_file = open('document_cloud_OCR.csv', 'w')
csv_file.seek(0)
csv_writer = unicodecsv.writer(csv_file)
csv_writer.writerow(["ID","OCR Text"])

with open('docIDs.csv', mode='r') as infile:
    reader = unicodecsv.reader(infile)
    with open('docIDs.csv', mode='r') as outfile:
        print "starting to write"
        writer = unicodecsv.writer(outfile)
        print "starting to read"
        request_pks = {rows[0]:rows[0] for rows in reader}
        print "all read"
        print request_pks


for document_id in request_pks:
    print "Working on request " + str(document_id)
    try:
        obj = client.documents.get(document_id)
        OCR = obj.full_text
        csv_writer.writerow([document_id,OCR])
    except Exception as e:
        print e
