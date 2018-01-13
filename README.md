Work Project - 

I'll update this more shortly -

Basically the whole thing takes all machine reports, and gets the MTTR (Mean time to repair) and MTBR (Mean time between repairs) 
and gives a quarterly status. 

WIP

To recreate from scratch:

In command-prompt or powershell, create the database by typing sqlite3 name_of_database.db

Run createTableMisc.py to create the quarterly tables, machine table, reports table

Run machineUpdate.py to update the machines table

Run reportUpdate.py to add all reports to the reports table

Run mtbrMachineUpdate.py to update equipment list in all quarterly tables

Run mtbr quarterly.py for each quarter that you need info for

Profit

