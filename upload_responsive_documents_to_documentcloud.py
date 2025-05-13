""" 
    Sample script that uses the MuckRock and DocumentCloud APIs
    to upload all of the documents from a MuckRock FOIA request
    to a project on DocumentCloud

"""
import os
from muckrock import MuckRock
from documentcloud import DocumentCloud

# Safely store our credentials in local environment variables
# so that we don't expose them to the internet
ma_user = os.environ.get("MA_USER")
ma_pass = os.environ.get("MA_PASSWORD")

# Start our MuckRock requests client
mr_client = MuckRock(ma_user, ma_pass)

# Prompt the user to enter a request ID they'd like to capture documents from
request_id = input("Please enter the request ID you'd like to download: ")
request = mr_client.requests.retrieve(request_id)

# Retrieves all of the communications from the request
comms_list = request.get_communications()

all_files = []

# For each communication, if there is an attached file, add the file to a list.
for comm in comms_list:
    files = list(comm.get_files())
    if files:  # Filters out comms with no actual files
        all_files.extend(files)

# Build out a list of file URLs we can use to upload to DocumentCloud
file_urls = []
for file in all_files:
    file_urls.append(file.ffile)

# Start our DocumentCloud client
dc_client = DocumentCloud(ma_user, ma_pass)

# Prompt our user for a project name
project_name = input("What would you like to name this project?")

# Create the project
project = dc_client.projects.create(project_name)

# Upload all of the files to our DocumentCloud project
our_docs = dc_client.documents.upload_urls(file_urls, projects=[project.id])
