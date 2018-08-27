#!/usr/bin/env python2
# -- coding: utf-8 --

import urllib
import unicodecsv as csv
from datetime import datetime, timedelta
import os.path
import requests
import json
import markdown
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from utils import get_api_key

mondayNotes = open("mondaynotes.md", 'w')

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'
headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}

page = 1
days = 7

staff_names = (
"JPat Brown",
"Caitlin Russell",
"Beryl Lipton",
"Jessie Gomez",
"Mitchell Kotler",
"Dylan Freedman",
"Aron Pilhofer",
"Michael Morisy"
)

class staffer_log:
	goal1 = ""
	goal2 = ""
	goal3 = ""
	goal1data = []
	goal2data = []
	goal3data = []
	tasks = []

def getWeeklyUpdates(staffer):
	print "Working on the goals progress the past week for " + staffer
	next_ = url + 'assignment-responses/?crowdsource=25&ordering=-id'

	day = 0
	page = 1
	while day < 1 and next_ is not None:
		r = requests.get(next_, headers=headers)
		try:
			json = r.json()
			next_ = json['next']
			for datum in json['results']:
				if datum["user"] == staffer:
					if day == 0:
						submitter = staffer_log()
						submitter.goal1 = [datum][0]['values'][0]['value']
						submitter.goal2 = [datum][0]['values'][2]['value']
						submitter.goal3 = [datum][0]['values'][4]['value']
						submitter.goal1data = [datum["values"][1]['value']]
						submitter.goal2data = [datum["values"][3]['value']]
						submitter.goal3data = [datum["values"][5]['value']]
						if datum["values"][16]['value'] is not None:
							submitter.tasks.append(datum["values"][16]['value'])
						if datum["values"][17]['value'] is not None:
							submitter.tasks.append(datum["values"][17]['value'])
						if datum["values"][18]['value'] is not None:
							submitter.tasks.append(datum["values"][18]['value'])
						if datum["values"][19]['value'] is not None:
							submitter.tasks.append(datum["values"][19]['value'])
						if datum["values"][20]['value'] is not None:
							submitter.tasks.append(datum["values"][20]['value'])
					else:
						submitter.goal1data.insert(0, datum["values"][1]['value'])
						submitter.goal2data.insert(0, datum["values"][3]['value'])
						submitter.goal3data.insert(0, datum["values"][5]['value'])
					day += 1
			print 'Page %d of %d' % (page, json['count'] / 10 + 1)
			page += 1
		except Exception as e:
			print e

	return submitter

def getStats():
	url = 'https://www.muckrock.com/api_v1/'

	next_ = url + 'statistics'

	fields = (
	"date",
	"num_crowdsource_responded_users",
	"total_crowdsource_responses",
	"project_users",
	"requests_processing_days",
	"total_active_org_members",
	"pro_users",
	"total_requests",
	"num_crowdsource_responded_users",
	"total_crowdsource_responses",
	"total_crowdsources",
	"total_pages",
	"total_users",
	)

	page = 1

	csv_file = open('stats.csv', 'w')
	csv_file.seek(0)
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(fields)

	while next_ is not None:
	    r = requests.get(next_, headers=headers)
	    try:
	        json = r.json()
	        next_ = json['next']
	        for datum in json['results']:
	            csv_writer.writerow([datum[field] for field in fields])
	        print 'Page %d of %d' % (page, json['count'] / 20 + 1)
	        page += 1
	    except Exception as e:
	        print e


def emojiTranslate(confidence):
		print "Confidence is " + str(confidence)
		if confidence is "1":
				return " 😵"
		if confidence is "3":
				return " 🙀"
		if confidence is "5":
				return " 😐"
		if confidence is "7":
				return " 🙂"
		if confidence is "10":
				return " Why doesn't this work?"
		return " 💯"

if os.path.isfile('check_in.csv'):
	with open('check_in.csv') as csvfile:
		# reader = csv.DictReader(csvfile)
		# mondayNotes.writelines("## Key Stats:\n")
		# mondayNotes.writelines("---\n\n")
		# mondayNotes.writelines("## MuckRock:\n")
		# stats = getStats()

		proData = pd.read_csv('stats.csv').set_index("date").iloc[::-1].tail(30)

		proData["pro_users"].plot(figsize=(6, 1))

		proData["total_active_org_members"].plot(figsize=(6, 1))
		x_max = int(max(plt.xticks()[0]))
		plt.title('Org & Pro Users')
		plt.savefig('org_and_pro_user_graph.png' , bbox_inches="tight")

		plt.close()

		dataForNumbers = pd.read_csv('stats.csv').set_index("date")

		mondayNotes.writelines("# Numbers \n")
		mondayNotes.writelines("| Stat | Past Week | Week Before | Weekly Average* | % of Goal | Graph \n")
		mondayNotes.writelines("|---|---|---|---|---|---|---|\n")
		mondayNotes.writelines("| Pro Users | " + str(int(dataForNumbers.iloc[0]["pro_users"])) + " | " + str(int(dataForNumbers.iloc[7]["pro_users"])) + " |   |   | | |\n")
		mondayNotes.writelines("| Organizational Users | " + str(dataForNumbers.iloc[0]["total_active_org_members"]) + " | " + str(dataForNumbers.iloc[7]["total_active_org_members"]) + " |   |   | | | \n")
		mondayNotes.writelines("| Combined Premium | " + str(dataForNumbers.iloc[0]["total_active_org_members"] + dataForNumbers.iloc[0]["pro_users"]) + " | " + str(dataForNumbers.iloc[7]["total_active_org_members"] + dataForNumbers.iloc[7]["pro_users"]) + " |   |   | | | \n")
		mondayNotes.writelines("| New Assignments | " + str(dataForNumbers.iloc[0]["total_crowdsource_responses"] - dataForNumbers.iloc[7]["total_crowdsource_responses"]) + "| " + str(int(dataForNumbers.iloc[7]["total_crowdsource_responses"] - dataForNumbers.iloc[14]["total_crowdsource_responses"])) + "  | " + str((dataForNumbers.iloc[0]["total_crowdsource_responses"] - dataForNumbers.iloc[83]["total_crowdsource_responses"])/12) + " |   | | |\n")
		mondayNotes.writelines("| New Assignment Users | " + str(int(dataForNumbers.iloc[0]["num_crowdsource_responded_users"] - dataForNumbers.iloc[7]["num_crowdsource_responded_users"])) + "| " + str(int(dataForNumbers.iloc[7]["num_crowdsource_responded_users"] - dataForNumbers.iloc[14]["num_crowdsource_responded_users"])) + "  | " + str(int((dataForNumbers.iloc[0]["num_crowdsource_responded_users"] - dataForNumbers.iloc[83]["num_crowdsource_responded_users"]))/12) + " |  | |  |\n")
		mondayNotes.writelines("| Requests | " + str(dataForNumbers.iloc[0]["total_requests"] - dataForNumbers.iloc[7]["total_requests"]) + "| " + str(dataForNumbers.iloc[7]["total_requests"] - dataForNumbers.iloc[14]["total_requests"]) + "  | " + str(int(dataForNumbers.iloc[0]["total_requests"] - dataForNumbers.iloc[83]["total_requests"]/12)) + " |  |||| |\n")





		mondayNotes.writelines("---\n")
		mondayNotes.writelines("\n")

		for staffer in staff_names:
			staffer_data = getWeeklyUpdates(staffer)
			mondayNotes.writelines("\n## " + staffer + "\n")
			mondayNotes.writelines("* " + staffer_data.goal1 + ": ")
			mondayNotes.writelines(emojiTranslate(str(staffer_data.goal1data[0])) + "\n")
			mondayNotes.writelines("* " + staffer_data.goal2 + ": ")
			mondayNotes.writelines(emojiTranslate(str(staffer_data.goal2data[0])) + "\n")
			mondayNotes.writelines("* " + staffer_data.goal3 + ": ")
			mondayNotes.writelines(emojiTranslate(str(staffer_data.goal3data[0])) + "\n")
			mondayNotes.writelines("\n### This week's Tasks \n\n")
			for task in staffer_data.tasks:
				mondayNotes.writelines("* " + task + "\n")


		print "All done, saving file."
		mondayNotes.close()

		markdownFile = open('mondaynotes.md', 'r')
		html = markdown.markdown(markdownFile.read())
		mondayNotes.close()

		text_file = open("report.html", "w")
		text_file.write(html)
		text_file.close()


else:
	print "Something went horribly wrong."
