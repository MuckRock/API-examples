# -- coding: utf-8 --
import urllib
import csv
from datetime import datetime, timedelta
import os.path


import requests
import csv
import json
#from pylab import *

from utils import get_api_key

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'
headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}

page = 1
days = 7

staff_names = (
"JPat Brown",
"Caitlin Russell",
"Beryl Lipton",
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

def getWeeklyUpdates(staffer):
	print "Working on the goals progress the past week for " + staffer
	next_ = url + 'assignment-responses/?crowdsource=25&ordering=-id'

	day = 0
	page = 1
	while day < days and next_ is not None:
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
	"num_crowdsource_responded_users",
	"total_crowdsource_responses"
	)

	r = requests.get(next_, headers=headers)
	results = []

	try:
		json = r.json()

		for field in fields:
			statistic = [field, json['results'][0][field], json['results'][0][field] - json['results'][6][field]]
			results.append(statistic)
	except Exception as e:
		print e
	return results


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
				return " 💯"
		return "❓"



if os.path.isfile('check_in.csv'):
	with open('check_in.csv') as csvfile:
		mondayNotes = open("mondaynotes.txt", 'w')
		print "Opening up the Monday notes."
		reader = csv.DictReader(csvfile)
		mondayNotes.writelines("Key Stats:\n")
		mondayNotes.writelines("==================\n\n")
		mondayNotes.writelines("MuckRock:\n")
		stats = getStats()
		for stat in stats:
				mondayNotes.writelines(stat[0] + " is currently at: " + str(stat[1]) + ", which has changed by " + str(stat[2]) + "\n")
		mondayNotes.writelines("==================\n")
		mondayNotes.writelines("\n")

		for staffer in staff_names:
			print "Here is what we've got on " + staffer + ":"
			staffer_data = getWeeklyUpdates(staffer)
			print staffer_data.goal1
			print staffer_data.goal1data
			print staffer_data.goal2
			print staffer_data.goal3
		print "All done, saving file."
		mondayNotes.close()
else:
	print "Something went horribly wrong."
