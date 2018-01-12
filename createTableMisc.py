import sqlite3

# Work Laptop
db = sqlite3.connect('C:\\Users\\ryan.visser\\maintenance.db')

# Surface Pro
# db = sqlite3.connect('C:\\Users\\ryanv\\maintenance.db')
cursor = db.cursor()

# For making the KPI table
cursor.execute("""CREATE TABLE Q1_2016(EQUIPMENT integer PRIMARY KEY,
	MTBR integer, MTTR integer, DT integer, COUNT integer)""")

# cursor.execute("""CREATE TABLE Q2_2019(EQUIPMENT integer PRIMARY KEY,
# 	MTBR integer, MTTR integer, DT integer, COUNT integer)""")

# cursor.execute("""CREATE TABLE Q3_2019(EQUIPMENT integer PRIMARY KEY,
# 	MTBR integer, MTTR integer, DT integer, COUNT integer)""")

# cursor.execute("""CREATE TABLE Q4_2019(EQUIPMENT integer PRIMARY KEY,
# 	MTBR integer, MTTR integer, DT integer, COUNT integer)""")



# For making the KPI table
# cursor.execute("""CREATE TABLE kpi(EQUIPMENT integer PRIMARY KEY,
# 	MTBR_ALL integer, MTBR_PREVIOUS integer, MTBR_YTD integer, MTBR_MONTH integer,
# 	MTTR_ALL integer, MTTR_PREVIOUS integer, MTTR_YTD integer, MTTR_MONTH integer,
# 	DT_ALL integer, DT_PREVIOUS integer, DT_YTD integer, DT_MONTH integer)""")

# For making machines table
# cursor.execute("""CREATE TABLE machines(EQUIPMENT integer PRIMARY KEY, DESCRIPTION text, PLANT integer,
# 	DEPARTMENT text, WORK_CENTER integer)""")

# For making reports table
# cursor.execute("""CREATE TABLE reports(NOTIFICATION integer PRIMARY KEY,
# 	DATE text, DESCRIPTION text, PLANT integer, DEPARTMENT text,
# 	WORK_CENTER integer, EQUIPMENT integer, BREAKDOWN text, DOWNTIME integer,
# 	REPORTED text, START_DATE text, START_TIME text, FINISH_DATE text,
# 	FINISH_TIME integer)""")


db.commit()

db.close()
