#!/usr/bin/env python2
# -- coding: utf-8 --

import urllib
import unicodecsv as csv
from datetime import timedelta
import datetime
import os.path
import requests
import json
import markdown
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mailchimp3 import MailChimp
import utils
from utils import get_api_key
from dateutil import parser


import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = utils.API_URL
token = utils.get_api_key()
headers = utils.get_headers(token)

mondayNotes = open("mondaynotes.md", 'w')

token = get_api_key()
mailChimpKey = raw_input('What is your Mailchimp API Key? ')

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
	previousTasks = []

def getWeeklyUpdates(staffer):
	print "Working on the goals progress the past week for " + staffer
	next_ = url + 'assignment-responses/?crowdsource=25&ordering=-id'
	day = 0
	page = 1
	submitter = staffer_log()
	submitter.tasks = []
	submitter.previousTasks = []
	while day < 1 and next_ is not None:
		r = requests.get(next_, headers=headers)
		try:
			json = r.json()
			next_ = json['next']
			for datum in json['results']:
				if datum["user"] == staffer:
					if day == 0:
						submitter.goal1 = [datum][0]['values'][0]['value']
						submitter.goal2 = [datum][0]['values'][2]['value']
						submitter.goal3 = [datum][0]['values'][4]['value']
						submitter.goal1data = [datum["values"][1]['value']]
						submitter.goal2data = [datum["values"][3]['value']]
						submitter.goal3data = [datum["values"][5]['value']]
						if datum["values"][16]['value']:
							submitter.tasks.append(datum["values"][16]['value'])
						if datum["values"][17]['value']:
							submitter.tasks.append(datum["values"][17]['value'])
						if datum["values"][18]['value']:
							submitter.tasks.append(datum["values"][18]['value'])
						if datum["values"][19]['value']:
							submitter.tasks.append(datum["values"][19]['value'])
						if datum["values"][20]['value']:
							submitter.tasks.append(datum["values"][20]['value'])
						if datum["values"][6]['value']:
							submitter.previousTasks.append(str(datum["values"][6]['value'] + ": " + datum["values"][7]['value']))
						if datum["values"][8]['value']:
							submitter.previousTasks.append(str(datum["values"][8]['value'] + ": " + datum["values"][9]['value']))
						if datum["values"][10]['value']:
							submitter.previousTasks.append(str(datum["values"][10]['value'] + ": " + datum["values"][11]['value']))
						if datum["values"][12]['value']:
							submitter.previousTasks.append(str(datum["values"][12]['value'] + ": " + datum["values"][13]['value']))
						if datum["values"][14]['value']:
							submitter.previousTasks.append(str(datum["values"][14]['value'] + ": " + datum["values"][15]['value']))
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

def getAssignmentStats():
	fields = (
	"id",
	"crowdsource",
	"user",
	"edit_user",
	"data",
	"datetime",
	"edit_datetime",
	"tags",
	"skip",
	"number",
	"flag",
	"gallery"
	)
	page = 1


	csv_file = open('assignment_responses.csv', 'w')
	csv_file.seek(0)
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(fields)
	next_ = url + 'assignment-responses'
	while next_ is not None:
	    r = requests.get(next_, headers=headers)
	    try:
	        json = r.json()
	        next_ = json['next']
	        for datum in json['results']:
	            csv_writer.writerow([datum[field] for field in fields])
	        print 'Page %d of %d' % (page, (json['count'] / 20) + 1)
	        page += 1
	    except Exception as e:
	        print e

	submissions = pd.read_csv('assignment_responses.csv')
	submissions.update(pd.to_datetime(submissions['datetime']).dt.strftime('%D')) # Drop the time from datetime
	submissions_by_day = submissions.pivot_table(index = ['datetime'], columns = "crowdsource", values = "id", aggfunc='count')
	submissions_by_day = submissions_by_day.fillna(0).cumsum()

	submissions_list = []
	for label in submissions_by_day:
		submissions_list.append([label,int(submissions_by_day[label].iloc[-1] - submissions_by_day[label].iloc[-8]),int(submissions_by_day[label].iloc[-8] - submissions_by_day[label].iloc[-15]),int(submissions_by_day[label].iloc[-1])])
	return submissions_list

def convertAssignmentLabel(assignmentNum):
	converter = {
		14: "Help us build an FCC complaint Twitter bot",
		35: "MuckRock Events and Talks",
		24: "Join the MuckRock FOIA Slack",
		25: "Monday Check In",
		30: "Help explore Donald Rumsfeld's Snowflakes",
		38: "Potential Stories and Records Issues",
		40: "Policing the Police: Domestic Violence",
		43: "Private Prison Feedback Line.",
		72: "What should we know?",
		73: "MuckRock Editorial Internship Application",
		74: "Municipal Investments",
		75: "What should we know about inmate firefighters?",
		78: "Caloocan First Pass",
		42: "Help us dig through the CIA's declassified archives.",
		44: "Sunshine Spotlight: Massachusetts",
		47: "Phone Calls from Prison",
		66: "Add to the Subjects Matter: FBI Files Project",
		79: "FOIA 101 Tip Line",
		76: "Tell us about your FOIA Fees!",
		83: "Help read the Brett Kavanaugh confirmation hearing files",
		85: "College Cola Contract Crowdsource",
		89: "Test"
		}
	if assignmentNum in converter:
		print converter[assignmentNum]
		return converter[assignmentNum]
	else:
		return str(int(assignmentNum))

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
		if confidence == "1":
				return " 😵"
		if confidence == "3":
				return " 🙀"
		if confidence == "5":
				return " 😐"
		if confidence == "7":
				return " 🙂"
		if confidence == "10":
				return " 💯"
		return " ?"

def getRecentCampaigns():
	campaign_data = []
	client = MailChimp(mc_api=mailChimpKey)
	today = datetime.date.today()
	margin = datetime.timedelta(days = 7)
	campaigns = client.campaigns.all(get_all=True)


	for campaign in campaigns["campaigns"]:
		try:
			if today - margin <= datetime.datetime.strptime(campaign["send_time"][:10], "%Y-%m-%d").date() <= today:
				print "Matching campaign:"
				print "URL: " + campaign["archive_url"]
				campaign_data.append([campaign["send_time"][:10], str(campaign['emails_sent']), campaign["recipients"]["list_name"], str(campaign["settings"]["subject_line"]), str(int(campaign['report_summary']["open_rate"]*100)) + "%", str(int(campaign['report_summary']["click_rate"]*100)) + "%",  campaign["archive_url"]])
				print "Current data is /n" + campaign_data
		except:
			print "Looks like no campaign date or another issue"
	print campaign_data
	return campaign_data

newsletterData = getRecentCampaigns()
getStats()

dataForNumbers = pd.read_csv('stats.csv').set_index("date")
dataForDocumentCloud = pd.read_csv('docstats.csv').set_index("day")

mondayNotes.writelines("# Numbers \n")
mondayNotes.writelines("## MuckRock \n")

mondayNotes.writelines("| Stat | Past Week | Week Before | Weekly Average* | vs. Goal \n")
mondayNotes.writelines("|---|---|---|---|---|---|---|\n")
mondayNotes.writelines("| Pro Users | " + str(int(dataForNumbers.iloc[0]["pro_users"])) + " | " + str(int(dataForNumbers.iloc[7]["pro_users"])) + " |   |   | |\n")
mondayNotes.writelines("| Organizational Users | " + str(int(dataForNumbers.iloc[0]["total_active_org_members"])) + " | " + str(int(dataForNumbers.iloc[7]["total_active_org_members"])) + " |   |    | | \n")
mondayNotes.writelines("| Combined Premium | " + str(int(dataForNumbers.iloc[0]["total_active_org_members"] + dataForNumbers.iloc[0]["pro_users"])) + " | " + str(int(dataForNumbers.iloc[7]["total_active_org_members"] + dataForNumbers.iloc[7]["pro_users"])) + " |     | " + str(int((dataForNumbers.iloc[0]["total_active_org_members"] + dataForNumbers.iloc[0]["pro_users"]) / 229 * 100)) + "% (Goal: 229) | \n")
mondayNotes.writelines("| New Assignments | " + str(int(dataForNumbers.iloc[0]["total_crowdsource_responses"] - dataForNumbers.iloc[7]["total_crowdsource_responses"])) + "| " + str(int(dataForNumbers.iloc[7]["total_crowdsource_responses"] - dataForNumbers.iloc[14]["total_crowdsource_responses"])) + "  | " + str(int(dataForNumbers.iloc[0]["total_crowdsource_responses"] - dataForNumbers.iloc[83]["total_crowdsource_responses"]/12)) + " |   " + str(int(dataForNumbers.iloc[0]["total_crowdsource_responses"] / 3000 * 100)) + "% (" + str(int(dataForNumbers.iloc[0]["total_crowdsource_responses"])) + " out of 3000) |\n")
mondayNotes.writelines("| New Assignment Users | " + str(int(dataForNumbers.iloc[0]["num_crowdsource_responded_users"] - dataForNumbers.iloc[7]["num_crowdsource_responded_users"])) + "| " + str(int(dataForNumbers.iloc[7]["num_crowdsource_responded_users"] - dataForNumbers.iloc[14]["num_crowdsource_responded_users"])) + "  | " + str(int((dataForNumbers.iloc[0]["num_crowdsource_responded_users"] - dataForNumbers.iloc[83]["num_crowdsource_responded_users"]))/12) + " |  | | \n")
mondayNotes.writelines("| Requests | " + str(int(dataForNumbers.iloc[0]["total_requests"] - dataForNumbers.iloc[7]["total_requests"])) + "| " + str(int(dataForNumbers.iloc[7]["total_requests"] - dataForNumbers.iloc[14]["total_requests"])) + "  | " + str(int((dataForNumbers.iloc[0]["total_requests"] - dataForNumbers.iloc[83]["total_requests"])/12)) + " |  ||||\n")

mondayNotes.writelines("## DocumentCloud \n")

mondayNotes.writelines("| Stat | Past Week | Week Before | Weekly Average* | vs. Goal \n")
mondayNotes.writelines("|---|---|---|---|---|---|---|\n")
print "accounts is " + str(dataForDocumentCloud.iloc[0]["accounts"])
mondayNotes.writelines("| New Accounts | " + str(int(dataForDocumentCloud.iloc[0]["accounts"]-dataForDocumentCloud.iloc[7]["accounts"])) + " | " + str(int(dataForDocumentCloud.iloc[7]["accounts"]-dataForDocumentCloud.iloc[14]["accounts"])) + " | " + str(int((dataForDocumentCloud.iloc[0]["accounts"] - dataForDocumentCloud.iloc[83]["accounts"])/12)) + " |   | |\n")
mondayNotes.writelines("| Active Accounts | " + str(int(dataForDocumentCloud.iloc[0]["active accounts"])) + " | " + str(int(dataForDocumentCloud.iloc[7]["active accounts"])) + " | |   | |\n")
mondayNotes.writelines("| New Pages | " + str(int(dataForDocumentCloud.iloc[0]["total pages"]-dataForDocumentCloud.iloc[7]["total pages"])) + " | " + str(int(dataForDocumentCloud.iloc[7]["total pages"]-dataForDocumentCloud.iloc[14]["total pages"])) + " | " + str(int((dataForDocumentCloud.iloc[0]["total pages"] - dataForDocumentCloud.iloc[83]["total pages"])/12)) + " |   | |\n")
mondayNotes.writelines("| New Public Pages | " + str(int(dataForDocumentCloud.iloc[0]["total public pages"]-dataForDocumentCloud.iloc[7]["total public pages"])) + " | " + str(int(dataForDocumentCloud.iloc[7]["total public pages"]-dataForDocumentCloud.iloc[14]["total public pages"])) + " | " + str(int((dataForDocumentCloud.iloc[0]["total public pages"] - dataForDocumentCloud.iloc[83]["total public pages"])/12)) + " |   | |\n")
mondayNotes.writelines("| New Orgs | " + str(int(dataForDocumentCloud.iloc[0]["total orgs"]-dataForDocumentCloud.iloc[7]["total orgs"])) + " | " + str(int(dataForDocumentCloud.iloc[7]["total orgs"]-dataForDocumentCloud.iloc[14]["total orgs"])) + " | " + str(int((dataForDocumentCloud.iloc[0]["total orgs"] - dataForDocumentCloud.iloc[83]["total orgs"])/12)) + " |   | |\n")


mondayNotes.writelines("\* Weekly average for last 12 weeks\n")


mondayNotes.writelines("\n---\n\n")

mondayNotes.writelines("# Editorial \n")

mondayNotes.writelines("| Day | Piece | Author |  \n")
mondayNotes.writelines("|---|---|---|\n")
mondayNotes.writelines("| Monday | Release Notes | Michael and Mitch |\n")
mondayNotes.writelines("| Friday | News Round Up | TBA |\n")
mondayNotes.writelines("---\n\n")

mondayNotes.writelines("# Newsletters \n")
mondayNotes.writelines("## Last Week \n")

mondayNotes.writelines("| Day | List Size | List | Subject Line | Open % | Click % |  \n")
mondayNotes.writelines("|---|---|---|---|---|---|\n")
for newsletter in newsletterData:
	mondayNotes.writelines("| " +  newsletter[0] + " | " +  newsletter[1] + " | " +  newsletter[2] + " | [" +  newsletter[3] + "](" + newsletter[6] +  ") | " +  newsletter[4] + " | " +  newsletter[5] + " |\n")

mondayNotes.writelines("## This Week \n")

mondayNotes.writelines("| Day | Newsletter | Editor |  \n")
mondayNotes.writelines("|---|---|---|\n")
mondayNotes.writelines("| Monday | Subjects Matter | JPat |\n")
mondayNotes.writelines("| Tuesday | Release Notes | Michael |\n")
mondayNotes.writelines("| Wednesday | Site Newsletter |  |\n")
mondayNotes.writelines("| Friday | Slack | Cynthia |\n")

mondayNotes.writelines("# Assignments \n")


mondayNotes.writelines("| Assignment | Submissions Week | Week Before | Total |\n")
mondayNotes.writelines("|---|---|---|---|\n")
#
assignment_stats = getAssignmentStats()

for assignment in assignment_stats:
	if assignment[1] > 0 or assignment[2] > 0:
		mondayNotes.writelines("|" + convertAssignmentLabel(assignment[0]) + "| " + str(assignment[1]) + "|" + str(assignment[2]) +"|" + str(assignment[3]) + "|\n")
#
#

mondayNotes.writelines("---\n\n")
mondayNotes.writelines("\n# Weekly Tasks \n")


for staffer in staff_names:
	staffer_data = getWeeklyUpdates(staffer)
	mondayNotes.writelines("\n## " + staffer + "\n")
	mondayNotes.writelines("* " + staffer_data.goal1 + ": ")
	mondayNotes.writelines(emojiTranslate(str(staffer_data.goal1data[0])) + "\n")
	mondayNotes.writelines("* " + staffer_data.goal2 + ": ")
	mondayNotes.writelines(emojiTranslate(str(staffer_data.goal2data[0])) + "\n")
	mondayNotes.writelines("* " + staffer_data.goal3 + ": ")
	mondayNotes.writelines(emojiTranslate(str(staffer_data.goal3data[0])) + "\n")

	mondayNotes.writelines("\n### Last week's Tasks \n")
	for task in staffer_data.previousTasks:
		mondayNotes.writelines("* " + task + "\n")
	mondayNotes.writelines("\n### This week's Tasks \n")
	for task in staffer_data.tasks:
		mondayNotes.writelines("* " + task + "\n")


mondayNotes.close()

#markdownFile = open('mondaynotes.md', 'r')
#html = markdown.markdown(markdownFile.read())
#mondayNotes.close()

#text_file = open("report.html", "w")
#text_file.write(html)
#open .text_file.close()
