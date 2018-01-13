#!/usr/bin/env python3

import sqlite3
import csv

''' This script updates the reports table in musashi.db.alias
it will ignore duplicates, so finding the latest report is not important
File must be saved as CSV, and must have the headers set up specifically'''

# Create a database in RAM
# db = sqlite3.connect(':memory:')
# Work Laptop
# db = sqlite3.connect('H:\\Projects\\maintenance.db')

# Surface Pro
db = sqlite3.connect('C:\\Projects\\Musashi\\maintenance.db')

# Get a cursor object
cursor = db.cursor()

# Counters to see what reports were added
count_add = 0
count_ignore = 0

# NOTIFICATION[0] - DATE[1] - DESCRIPTION[2] - PLANT[3] - DEPARTMENT[4]
# WORK_CENTER [5] - EQUIPMENT[6] - BREAKDOWN[7] - DOWNTIME[8] - REPORTED[10] - 
# START_DATE[11] - START_TIME[12] - FINSIH_DATE[13] - FINISH_TIME[14]
with open('C:\\Projects\\Musashi\\reports.csv') as f: # Need to change path if using on Work PC
    csvreader = csv.reader(f)
    next(csvreader)
    for row in csvreader:
        try:
            cursor.execute('''INSERT INTO reports(NOTIFICATION, DATE,
            	DESCRIPTION, PLANT, DEPARTMENT, WORK_CENTER, EQUIPMENT,
            	BREAKDOWN, DOWNTIME, REPORTED, START_DATE, START_TIME, 
                FINISH_DATE, FINISH_TIME) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6], row[7], row[8], row[10], row[11], row[12],
                            row[13], row[14]))
            count_add += 1
        except sqlite3.IntegrityError:
            count_ignore += 1
            pass
db.commit()

print(str(count_add) + ' Reports added with ' +
      str(count_ignore) + ' reports ignored.')

db.close()
