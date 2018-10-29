import urllib
import csv
from datetime import datetime
import os.path

# To do:
# - Limit to X updates per day
# - Post tweets!
# - Screenshot
# - ???

csvNumber = 1
# deduplicate = True

print "Kicking off"

while csvNumber < 5:
    if not os.path.isfile('crest_lite_' + str(csvNumber) + '.csv'):
        urllib.urlretrieve('https://cdn.muckrock.com/files_static/crest_csv/crest_lite_' + str(csvNumber) + '.csv', 'crest_lite_' + str(csvNumber) + '.csv')
        print "We downloaded the CSV."
    else:
        print "We already have that CSV."
    with open('crest_lite_' + str(csvNumber) + '.csv') as csvfile:
        print "Opening Crest Lite " + (str(csvNumber))
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['publication_date'] != '' and 'Diary' in row['title']:
                print "Found a diary!"
                datetime_object = datetime.strptime(row['publication_date'], '%B %d, %Y')
                csv_file = open('diary ' + str(datetime_object.strftime('%m')) + '-' + str(datetime_object.strftime('%d')) + '-' + str(datetime_object.strftime('%Y')) + '.csv', 'a')
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(
#            else:
#                print "No date or not a diary"
        print "All done."
        csvNumber += 1
