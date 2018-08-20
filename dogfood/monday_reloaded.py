# -- coding: utf-8 --
import urllib
import csv
from datetime import datetime, timedelta
import os.path
import requests
import csv
import json
import markdown


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

stats = pd.read_csv('stats.csv')

## should be able to graph what we need to from that 

from utils import get_api_key

token = get_api_key()
url = 'https://www.muckrock.com/api_v1/'
headers = {'Authorization': 'Token %s' % token, 'content-type': 'application/json'}

page = 1
days = 7

staff_names = (
"Caitlin Russell",
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

def chartData(data, name, filename):
		fig, ax = plt.subplots()
		plt.plot(data, color='k')
		ax.set_title(name)
		for k,v in ax.spines.items():
			v.set_visible(False)
#		ax.set_xticks([])
		ax.set_yticks([])
		plt.savefig(filename +'.png')
#		ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
#		ax.bar([0, 1], [0, 100], 0.25)
#		ax.spines['right'].set_color('none')
#		ax.spines['top'].set_color('none')
#		ax.xaxis.set_ticks_position('bottom')
		ax.set_xticks([0, 1])
		ax.set_xlim([-0.5, 8])
		ax.set_ylim([-1, 13])


if os.path.isfile('check_in.csv'):
	with open('check_in.csv') as csvfile:
		mondayNotes = open("mondaynotes.md", 'w')
		reader = csv.DictReader(csvfile)
		mondayNotes.writelines("## Key Stats:\n")
		mondayNotes.writelines("---\n\n")
		mondayNotes.writelines("## MuckRock:\n")
		stats = getStats()
		for stat in stats:
				mondayNotes.writelines(stat[0] + " is currently at: " + str(stat[1]) + ", which has changed by " + str(stat[2]) + "\n")
		mondayNotes.writelines("---\n")
		mondayNotes.writelines("\n")

		for staffer in staff_names:
			staffer_data = getWeeklyUpdates(staffer)
			mondayNotes.writelines("## " + staffer + "\n")
			mondayNotes.writelines(staffer_data.goal1 + "\n")
			chartData(staffer_data.goal1data, staffer_data.goal1, staffer + "goal1")
 			mondayNotes.writelines(" ![](" + staffer + "goal1.png)\n")

			mondayNotes.writelines(staffer_data.goal2)
			chartData(staffer_data.goal1data, staffer_data.goal2, staffer + "goal2")
			mondayNotes.writelines(" ![](" + staffer + "goal2.png)\n")

			mondayNotes.writelines(staffer_data.goal3)
			chartData(staffer_data.goal1data, staffer_data.goal3, staffer + "goal3")
			mondayNotes.writelines(" ![](" + staffer + "goal3.png)\n")

		print "All done, saving file."
		mondayNotes.close()

		markdownFile = open('mondaynotes.md', 'r')
		html = markdown.markdown(markdownFile.read())

		text_file = open("report.html", "w")
		text_file.write(html)
		text_file.close()


else:
	print "Something went horribly wrong."
