#!/usr/bin/env python3

import sqlite3
import csv

# Create a database in RAM
# db = sqlite3.connect(':memory:')
# Work Laptop
# db = sqlite3.connect('H:\\Projects\\maintenance.db')

# Surface Pro
db = sqlite3.connect('C:\\Projects\\Musashi\\maintenance.db')

# Get a cursor object
cursor = db.cursor()

# Counters to see what equipment was added
count_ignore = 0
count_add = 0

# (0, 'EQUIPMENT', 'integer', 0, None, 1)
# (1, 'DESCRIPTION', 'text', 0, None, 0)
# (2, 'PLANT', 'integer', 0, None, 0)
# (3, 'DEPARTMENT', 'text', 0, None, 0)
# (4, 'WORK_CENTER', 'integer', 0, None, 0)

# Equipment[0],Description[1],Location[2],Cost Center[3],Plant[4]

with open('C:\\Projects\Musashi\\machine list.csv') as f: # Change if running on work PC
        # reader = csv.reader(f)
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            try:
                cursor.execute('''INSERT INTO machines(EQUIPMENT, DESCRIPTION, PLANT, DEPARTMENT) VALUES(?,?,?,?)''', (row[0], row[1], row[4], row[2]))
                count_add += 1
            except MySQLdb.IntegrityError:
                pass
db.commit()

print(str(count_add) + ' Machines were added')

db.close()
