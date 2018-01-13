import sqlite3
import time
from datetime import datetime, timedelta

start = time.time()

# Work Laptop
db = sqlite3.connect('H:\\Projects\\maintenance.db')

# Surface Pro
# db = sqlite3.connect('C:\\Projects\\Musashi\\maintenance.db')

cursor = db.cursor()

# KPI Table Details
# (0, 'EQUIPMENT', 'integer', 0, None, 1)
# (1, 'MTBR_ALL', 'integer', 0, None, 0)t
# (2, 'MTBR_PREVIOUS', 'integer', 0, None, 0)
# (3, 'MTBR_YTD', 'integer', 0, None, 0)
# (4, 'MTTR_ALL', 'integer', 0, None, 0)
# (5, 'MTTR_PREVIOUS', 'integer', 0, None, 0)
# (6, 'MTTR_YTD', 'integer', 0, None, 0)
# (7, 'DT_ALL', 'integer', 0, None, 0)
# (8, 'DT_PREVIOUS', 'integer', 0, None, 0)
# (9, 'DT_YTD', 'integer', 0, None, 0)

# Variables
downtime = 0
downtime_avg = 0
count = 0
time_between = 0
time_between_avg = 0
start_date = ''
start_time = ''
finish_date = ''
finish_time = ''

# d1 gets previous YEAR
d1 = datetime.now().date() - timedelta(days=365)
d1 = '%' + d1.strftime("%Y") + '%'
# d2 gets current YEAR
d2 = datetime.now().date()
d2 = '%' + d2.strftime("%Y") + '%'
# d3 gets today's date and time
d3_date = datetime.now().date()
d3_date = d3_date.strftime("%m/%d/%Y")
d3_time = datetime.now().time()
d3_time = d3_time.strftime("%H:%M:%S")
# d4 gets previous years starting date - Unused as of now
d4_date = datetime.now().date() - timedelta(days=365)
d4_date = '01/01/' + d4_date.strftime("%Y")
d4_time = '00:00:00'
# d5 gets this years starting date - Unused as of now
d5_date = datetime.now().date()
d5_date = '01/01/' + d5_date.strftime("%Y")
d5_time = '00:00:00'

''' time_difference function takes the start date, start time, finish date,
finish time, and returns the hours between the two. Returns absolute (positive
number). Python doesn't like 24:00:00, so times will be changed tob23:59:59 '''


def time_difference(start_date, start_time, finish_date, finish_time):
    datetimeFormat = '%m/%d/%Y %H:%M:%S'
    if start_time == '24:00:00':
        start_time = '23:59:59'
    elif finish_time == '24:00:00':
        finish_time = '23:59:59'
    time1 = ''.join(start_date + ' ' + start_time)
    time2 = ''.join(finish_date + ' ' + finish_time)
    timedelta = datetime.strptime(
        time1, datetimeFormat) - datetime.strptime(
        time2, datetimeFormat)
    days = timedelta.days * 86400 + timedelta.seconds
    hours = abs(days / 3600)
    return hours


cursor.execute('''SELECT EQUIPMENT from KPI''')

rows = cursor.fetchall()
# Runs ALL TIME report
for row in rows:
    machine = row[0]
    try:
        cursor.execute('''SELECT DOWNTIME, START_DATE, START_TIME, FINISH_DATE,
			 FINISH_TIME FROM REPORTS WHERE BREAKDOWN = 'X' AND EQUIPMENT = ? ''', (machine,))
    except:
        print('Something went wrong when gathering reports from the database')
        break
    results = cursor.fetchall()
    for row in results: # Iterates through each report for specified machine number
        downtime += row[0]
        count += 1
        if count == 1:
            if not row[3]:
                finish_date = row[1]
            else:
                finish_date = row[3]
            finish_time = row[4]
        else:
            start_date = row[1]
            start_time = row[2]
            time_between += time_difference(start_date,
                                            start_time, finish_date, finish_time)
            if not row[3]:
                finish_date = row[1]
            else:
                finish_date = row[3]
            finish_time = row[4]
    if count == 0:
        downtime_avg = downtime
        time_between_avg = time_between
    else:
        time_between += time_difference(d3_date,
                                        d3_time, finish_date, finish_time)
        downtime_avg = downtime / count
        time_between_avg = time_between / count
    try:
        cursor.execute('''UPDATE kpi SET DT_ALL = ?, MTTR_ALL = ?, MTBR_ALL = ? WHERE EQUIPMENT = ? ''', (round(
            downtime, 2), round(downtime_avg, 2), round(time_between_avg, 2), machine))
    except:
        print('Something went wrong when writing to the database.')
    downtime = 0
    downtime_avg = 0
    count = 0
    time_between = 0
    time_between_avg = 0

# Runs LAST YEARS report
for row in rows:
    machine = row[0]
    try:
        cursor.execute('''SELECT DOWNTIME, START_DATE, START_TIME, FINISH_DATE,
			 FINISH_TIME FROM REPORTS WHERE BREAKDOWN = 'X' AND EQUIPMENT = ? AND DATE LIKE ? ''', (machine, d1))
    except:
        print('Something went wrong when gathering reports from the database')
        break
    results = cursor.fetchall()
    for row in results: # Iterates through each report for specified machine number
        downtime += row[0]
        count += 1
        if count == 1: # If first time running through
            if not row[3]:
                finish_date = row[1]
            else:
                finish_date = row[3]
            finish_time = row[4]
            time_between += time_difference(d4_date, d4_time, row[1], row[2]) # Adds up time from start of the year
            count += 1
        else:
            start_date = row[1]
            start_time = row[2]
            time_between += time_difference(start_date, start_time, finish_date, finish_time)
            if not row[3]:
                finish_date = row[1]
            else:
                finish_date = row[3]
            finish_time = row[4]
    if count == 0:
        downtime_avg = downtime
        time_between_avg = time_between
    else:
        time_between += time_difference(d3_date,
                                        d3_time, finish_date, finish_time)
        downtime_avg = downtime / count
        time_between_avg = time_between / count
    try:
        cursor.execute('''UPDATE kpi SET DT_PREVIOUS = ?, MTTR_PREVIOUS = ?, MTBR_PREVIOUS = ? WHERE EQUIPMENT = ? ''', (round(
            downtime, 2), round(downtime_avg, 2), round(time_between_avg, 2), machine))
    except:
        print('Something went wrong when writing Previous Years information to the database.')
        break
    downtime = 0
    downtime_avg = 0
    count = 0
    time_between = 0
    time_between_avg = 0

# Runs YTD report
for row in rows: # Iterates through each report for specified machine number
    machine = row[0]
    try:
        cursor.execute('''SELECT DOWNTIME, START_DATE, START_TIME, FINISH_DATE,
			 FINISH_TIME FROM REPORTS WHERE BREAKDOWN = 'X' AND EQUIPMENT = ? AND DATE LIKE ? ''', (machine, d2))
    except:
        print('Something went wrong when gathering reports from the database')
        break
    results = cursor.fetchall()
    for row in results:
        downtime += row[0]
        count += 1
        if count == 1:
            if not row[3]:
                finish_date = row[1]
            else:
                finish_date = row[3]
            finish_time = row[4]
            time_between += time_difference(d5_date, d5_time, row[1], row[2]) # Adds up time from start of the year
            count += 1
        else:
            start_date = row[1]
            start_time = row[2]
            time_between += time_difference(start_date,
                                            start_time, finish_date, finish_time)
            if not row[3]:
                finish_date = row[1]
            else:
                finish_date = row[3]
            finish_time = row[4]
    if count == 0:
        downtime_avg = downtime
        time_between_avg = time_between
    else:
        time_between += time_difference(d3_date,
                                        d3_time, finish_date, finish_time)
        downtime_avg = downtime / count
        time_between_avg = time_between / count
    try:
        cursor.execute('''UPDATE kpi SET DT_YTD = ?, MTTR_YTD = ?, MTBR_YTD = ? WHERE EQUIPMENT = ? ''', (round(
            downtime, 2), round(downtime_avg, 2), round(time_between_avg, 2), machine))
    except:
        print('Something went wrong when writing Current Years information to the database.')
        break
    downtime = 0
    downtime_avg = 0
    count = 0
    time_between = 0
    time_between_avg = 0


db.commit()

db.close()

# Script timer
end = time.time()
print(end - start)
