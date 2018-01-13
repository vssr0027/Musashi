import sqlite3
import time
from datetime import datetime, timedelta
# import pdb; pdb.set_trace()

script_start = time.time()

# Work Laptop
# db = sqlite3.connect('H:\\Projects\\maintenance.db')

# Surface Pro
db = sqlite3.connect('C:\\Projects\\Musashi\\maintenance.db')

cursor = db.cursor()

# Variables
downtime = 0
downtime_avg = 0
count = 0
breakdowns = 0
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

# quarter dates without year
q1_start = '01/01/'
q1_end = '03/31/'
q2_start = '04/01/'
q2_end = '06/30/'
q3_start = '07/01/'
q3_end = '09/30/'
q4_start = '10/01/'
q4_end = '12/31/'

year = input('Enter the year: ')
quarter = input('Enter the quarter (Q1 - Q2 - Q3 - Q4): ')

# Getting the quarter start / finish date based on user input
if quarter.lower() == "q1":
    start = ''.join(q1_start + year)
    finish = ''.join(q1_end + year)
elif quarter.lower() == "q2":
    start = ''.join(q2_start + year)
    finish = ''.join(q2_end + year)
elif quarter.lower() == "q3":
    start = ''.join(q3_start + year)
    finish = ''.join(q3_end + year)
elif quarter.lower() == "q4":
    start = ''.join(q4_start + year)
    finish = ''.join(q4_end + year)
else:
    print(f'{quarter} is not a valid response. Please try again')

current_db = quarter.upper() + '_' + year



def time_difference(start_date, start_time, finish_date, finish_time):
    ''' time_difference function takes the start date, start time, finish date,
    finish time, and returns the hours between the two. Returns absolute (positive
    number). Python doesn't like 24:00:00, so times will be changed to 23:59:59 '''
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


cursor.execute(f'''SELECT EQUIPMENT from {current_db}''')

# DOWNTIME[0]
# START_DATE[1]
# START_TIME[2]
# FINISH_DATE[3]
# FINISH_TIME[4]


rows = cursor.fetchall()
# Currently runs last years report
for row in rows:
    machine = row[0]
    try:
        cursor.execute(f'''SELECT DOWNTIME, START_DATE, START_TIME, FINISH_DATE,
             FINISH_TIME, NOTIFICATION FROM REPORTS WHERE BREAKDOWN = 'X' AND EQUIPMENT = {machine}''')
    except:
        print('Something went wrong when gathering reports from the database')
        break
    results = cursor.fetchall()
    for row in results: # Iterates through each report for specified machine number
        if row[1] >= start and row[1] <= finish and year in row[1]:  # Checking if the report dates are in the quarter
            downtime += row[0]
            count += 1
            breakdowns += 1
            if count == 1: # If first time running through
                if not row[3]:  # If there is no finish date, the start date is substituted
                    finish_date = row[1]
                else:
                    finish_date = row[3]
                finish_time = row[4]
                time_between += time_difference(start, d4_time, row[1], row[2]) # Adds up time from start of the year
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
        else:
            continue
    if count == 0:
        downtime_avg = downtime
        time_between_avg = time_between
    else:
        time_between += time_difference(finish,
                                        d4_time, finish_date, finish_time)
        downtime_avg = downtime / breakdowns
        time_between_avg = time_between / count
        # print(f'{machine} {row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}') # testing
    try:
        cursor.execute(f'''UPDATE {current_db} SET DT = {round(downtime, 2)},
         MTTR = {round(downtime_avg, 2)}, MTBR = {round(time_between_avg, 2)},
          COUNT = {breakdowns} WHERE EQUIPMENT = {machine} ''')
    except:
        print('Something went wrong when writing Previous Years information to the database.')
        break
    downtime = 0
    downtime_avg = 0
    count = 0
    breakdowns = 0
    time_between = 0
    time_between_avg = 0


db.commit()
db.close()

# Script timer
script_end = time.time()
print(abs(script_start - script_end))


