#!/usr/bin/env python3

import sqlite3

# Work Laptop
# db = sqlite3.connect('C:\\Users\\ryan.visser\\musashi.db')

# Surface Pro
db = sqlite3.connect('C:\\Users\\ryanv\\musashi.db')
cursor = db.cursor()

cursor.execute("""SELECT * from kpi Natural Join machines where PLANT = 2220 and MTBR_YTD != 0 ORDER BY MTBR_YTD limit 10;""")
rows = cursor.fetchall()

# cursor.execute("""SELECT EQUIPMENT, MTBR_PREVIOUS, MTTR_PREVIOUS, DT_PREVIOUS, DESCRIPTION, DEPARTMENT from kpi Natural Join machines where PLANT = 2220 and MTBR_PREVIOUS != 0 ORDER BY MTBR_PREVIOUS LIMIT 10;;""")
# rows = cursor.fetchall()





for row in rows:
	print(row)



db.commit()

db.close()