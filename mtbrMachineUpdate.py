#!/usr/bin/env python3

import sqlite3
import csv

''' This script updates the reports table in musashi.db.alias
it will ignore duplicates, so finding the latest report is not important
File must be saved as CSV, and must have the headers set up specifically'''

# Create a database in RAM
# db = sqlite3.connect(':memory:')


# Work Laptop
db = sqlite3.connect('C:\\Users\\ryan.visser\\maintenance.db')

# Surface Pro
# db = sqlite3.connect('C:\\Users\\ryanv\\maintenance.db')

# Get a cursor object
cursor = db.cursor()

# Counters to see what reports were added
count_add = 0
count_ignore = 0

# def table():
	# (0, 'EQUIPMENT', 'integer', 0, None, 1)
	# (1, 'MTBR_ALL', 'integer', 0, None, 0)
	# (2, 'MTBR_PREVIOUS', 'integer', 0, None, 0)
	# (3, 'MTBR_YTD', 'integer', 0, None, 0)
	# (4, 'MTTR_ALL', 'integer', 0, None, 0)
	# (5, 'MTTR_PREVIOUS', 'integer', 0, None, 0)
	# (6, 'MTTR_YTD', 'integer', 0, None, 0)
	# (7, 'DT_ALL', 'integer', 0, None, 0)
	# (8, 'DT_PREVIOUS', 'integer', 0, None, 0)
	# (9, 'DT_YTD', 'integer', 0, None, 0)

databases = ['Q1_2016', 'Q2_2016', 'Q3_2016', 'Q4_2016', 'Q1_2017', 'Q2_2017', 'Q3_2017', 'Q4_2017', 'Q1_2018', 'Q2_2018', 'Q3_2018', 'Q4_2018', 'Q1_2019', 'Q2_2019', 'Q3_2019', 'Q4_2019', ]


cursor.execute("""SELECT EQUIPMENT FROM machines""")
rows = cursor.fetchall()
for i in databases:
	for row in rows:
		try:
			cursor.execute(f'''INSERT INTO {i}(EQUIPMENT) VALUES(?)''', (row))
			count_add += 1
		except sqlite3.IntegrityError:
			count_ignore += 1
			pass




db.commit()

print(str(count_add) + ' Machines added with ' +
      str(count_ignore) + ' machines ignored.')

db.close()
