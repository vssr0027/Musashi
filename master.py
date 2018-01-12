
import sqlite3


# Work Laptop
db = sqlite3.connect('H:\\Projects\\maintenance.db')

# Surface Pro
# db = sqlite3.connect('C:\\Users\\ryanv\\musashi.db')
cursor = db.cursor()

# Will print a list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

holder = 0
print('Hit q + enter to quit')
while holder != 1:
    answer = input('From the above list, which table would you like to see?: ')
    if answer == 'q':
        holder += 1
        break
    # Will print all headers in a table
    for row in cursor.execute("pragma table_info('" + answer + "')").fetchall():
            print(row)

# cursor.execute("SELECT * FROM reports LIMIT 1;")
# print(cursor.fetchall())

db.commit()

db.close()
