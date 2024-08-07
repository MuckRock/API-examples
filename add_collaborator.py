#!/usr/bin/env python

import json

import requests

import utils

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

# set the IDs for the requests to change here
FOIA_IDS = []
# set the IDs for the users to add as editors here
EDITORS = []
# set the IDs for the users to add as viewers here
VIEWERS = []

for foia_id in FOIA_IDS:
    print(f"Updating request {foia_id}")
    response = requests.patch(
        f"{url}foia/{foia_id}/",
        headers=headers,
        json={
            "edit_collaborators": EDITORS,
            "read_collaborators": VIEWERS,
        },
    )
    response.raise_for_status()
