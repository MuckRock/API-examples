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

staff_names = (
"JPat Brown",
"Caitlin Russell",
"Beryl Lipton",
"Mitchell Kotler",
"Dylan Freedman",
"Aron Pilhofer",
"Michael Morisy"
)



def getWeeklyUpdates(staffer):
	print "Working on the goals progress the past week for " + staffer
	next_ = url + 'assignment-responses/?crowdsource=25&ordering=-id'
	r = requests.get(next_, headers=headers)
	json = r.json()
	staffer_log = []
	day = 0
	entry = 0
	while day <= 3:
		for goal in range(1,3): ## Need to add in succesful pagination
			print "Looking at entry " + str(entry)
			if json['results'][entry]["user"] == staffer:
				print "Found goal " + str(goal) + " update."
				print json['results'][entry]["values"][0]['value']
				if name in staffer_log["Goal #" + str(goal)]]:
				else:
					staffer_log["Goal #" + str(goal)]["name"] = json['results'][entry]["values"][0]['value']["name"]
				= json['results'][entry]["values"]
				print "Confidence for " + staffer + " was " + str(staffer_log["Quarterly Goal #" + goal][day])
				day += 1
				entry += 1
			else:
				print "No goals that time"
				entry += 1
	return staffer_log

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


print "Pulling check ins via API"




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
#			d = timedelta(row['datetime'],datetime.date.today())
#			if d(days)<5:
			print "Here is what we've got on " + staffer + ":"
			print getWeeklyUpdates(staffer)
#		misc = ["Upcoming in next four weeks", "Department FYSA", "user"]
#		misc = ["user"]
#		for section in misc:
#			mondayNotes.writelines(section + ":\n")
#			mondayNotes.writelines("==================\n")
#			for row in reader:
#				print "Investigating a row"
#				mondayNotes.writelines(row[section] + "__—" + row["user"] + "__\n")
		print "All done, saving file."
		mondayNotes.close()
else:
	print "Something went horribly wrong."
