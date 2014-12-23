#!/usr/bin/env python

import requests
import json
import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

# You can get the PK for the agency and jurisdiction using their API
# The agency you select must belong to the jurisdiction you select, or you will receive an error
USA_PK = 10
TEST_AGENCY_PK = 248

data = json.dumps({
    'jurisdiction': USA_PK,
    'agency': TEST_AGENCY_PK,
    'title': 'API Test File Request',
    'document_request': 'I would like the government\'s secret receipe for the world\'s best burrito',
    })

# The request will be saved as a draft if you do not have any requests left
r = requests.post(url + 'foia/', headers=headers, data=data)

print(r)
