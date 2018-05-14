# -- coding: utf-8 --
import urllib
import csv
from datetime import datetime, timedelta
import os.path


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
		print "Inspecting check_in.csv"
		mondayNotes = open("sundayreminder.txt", 'w')
		reader = csv.DictReader(csvfile)
		mondayNotes.writelines("New Goals + Last Week's Priorities:\n")
		mondayNotes.writelines("==================\n")
		mondayNotes.writelines("\n")

		for row in reader:
#			d = timedelta(row['datetime'],datetime.date.today())
#			if d(days)<5:
			if True:
				print "working on the update from " + row["user"]
				mondayNotes.writelines("\n\n" + row["user"] + "\n")
				mondayNotes.writelines("==================\n")
				mondayNotes.writelines("Quarterly Goals\n")
				mondayNotes.writelines("_______________\n")
				mondayNotes.writelines(row["Quarterly Goal #1"])
				mondayNotes.writelines(row["Quarterly Goal #2"])
				mondayNotes.writelines(row["Quarterly Goal #3"])

				mondayNotes.writelines("\n\nLast Week's Tasks" + "\n")
				mondayNotes.writelines("_______________" + "\n")
				task = 1
				try:
					while row["What's this week's prioritized task #" + str(task) + "?"] != "":
						mondayNotes.writelines("* " + row["What's this week's prioritized task #" + str(task) + "?"])
						task += 1
				except:
					print "no more tasks"
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
	print "The check_in.csv is missing."
