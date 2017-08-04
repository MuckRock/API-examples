import requests
import json
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

EXISTING_PKS = [] # If you've already filed with a given agency, or otherwise want to exclude it, include its ID here.


AGENCY_PKS = [248] # Agency ID 248 is a test agency under federal jurisdiction 10. This ID is subject to change, and will deduct requests from your account. Contact info@muckrock.com and we'll add them back.

AGENCY_PKS = filter(lambda x: x not in EXISTING_PKS, AGENCY_PKS)
DOCS = """
A copy of your reports that are:
Annual
Monthly
Bimonthly
"""
TITLE = 'Records Request' # Customize here for your project

for agency_pk in AGENCY_PKS:
    # get the jurisdiction
    r = requests.get(url + 'agency/{}/'.format(agency_pk), headers=headers)
    jurisdiction_pk = r.json()['jurisdiction']

    print 'Filing for {}...'.format(r.json()['name'])

    # get the template text
    r = requests.get(url + 'jurisdiction/{}/template/'.format(jurisdiction_pk), headers=headers)
    text = r.json()['text']

    # replace the text as required, such as if requests are permanently embargoed
    text = text.replace('<insert requested documents here>', DOCS)
    text = text.replace(
            'The requested documents will be made available to the general public, and t',
            'T',
            )
    print "Request Text: " + text
    # file the request
    data = json.dumps({
        'jurisdiction': jurisdiction_pk,
        'agency': agency_pk,
        'title': TITLE,
        'full_text': text,
        'requested_docs': DOCS,
        'embargo': True,
        })
    r = requests.post(url + 'foia/', headers=headers, data=data)
