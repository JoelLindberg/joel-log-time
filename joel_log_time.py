import sys
from datetime import date
from datetime import datetime
import sqlite3


DATABASE = "joel_log_time"
TABLE = "log_time"
DB_EXISTS = False
TABLE_EXISTS = False

con = sqlite3.connect(f"{DATABASE}.db")



# Check if database exists - otherwise create it
# Need to create this for sqlite to check for the database file instead
'''cnx.connect()
cur = cnx.cursor()
cur.execute("SHOW DATABASES;")
row = cur.fetchall()
# query result: a list containing tuples that contains the database name at index 0
for i in row:
    if i[0] == DATABASE:
        print(f"DB exists: {i[0]}")
        DB_EXISTS = True
        break

if DB_EXISTS == False:
    cur = cnx.cursor()
    cur.execute(f"CREATE DATABASE {DATABASE};")
    print("Created DB")

cnx.disconnect()'''



# Check if table exists - otherwise create it
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master")
r = cur.fetchall()

for i in r:
    if i[0] == "log_time":
        TABLE_EXISTS = True
        print(f"Table exists: {i[0]}")

if TABLE_EXISTS == False:
    tables = f"""CREATE TABLE {TABLE} (
        log_id INTEGER PRIMARY KEY,
        logged_date date,
        action varchar(3),
        log_time varchar(5),
        comment varchar(30)
        );"""
    # in/out <- 3
    #15:50 <- 5
    cur.execute(tables)
    print("Created table")

if len(sys.argv) == 1:
    # GET SALDO
    # This is where main logic will end up

    cur = con.cursor()
    cur.execute(f"SELECT log_id, logged_date, action, log_time, comment FROM {TABLE} WHERE logged_date = '2023-11-23' ORDER BY log_time;")
    r = cur.fetchall()
    #print(r)
    
    # need a tmp data structure for calculation - define a model for this later?
    logged = []
    for i in r:
        row = {}
        row["log_id"] = i[0]
        row["date"] = i[1]
        row["action"] = i[2]
        row["log_time"] = i[3]
        row["comment"] = i[4]
        logged.append(row)
    print(logged)

    # print our date objects we are working with
    dates = []
    d_timedelta = []
    previous_action = ""
    idx = 0
    for i in logged:
        date = datetime.fromisoformat(f'{str(i["date"])}T{i["log_time"]}')
        print(f'{date}, {i["action"]}')
        dates.append(datetime.fromisoformat(f'{str(i["date"])}T{i["log_time"]}'))

        if i["action"] == "out" and previous_action == "in":
            d_timedelta.append(dates[idx] - dates[idx - 1])
        elif i["action"] == "in":
            previous_action = "in"

        idx += 1
        '''day_total = dates[1] - dates[0]
        row["day_total"] = day_total'''
    #date.fromisoformat()
    
    idx = 0
    while idx < len(d_timedelta):
        print(f"Diff: {d_timedelta[idx]}")
        d = d_timedelta[idx] + d_timedelta[idx + 1]
        idx += 2
    print(f"Total = {d}")
    print(d_timedelta[0] + d_timedelta[1])
    
    # difference between them
    # returns a timedelta object?
    print(logged)
    #print(dates[1] - dates[0])




elif sys.argv[1] == "in":
    # IN
    # Add guard against adding IN after IN - Only allow pattern: IN -> UT -> IN -> UT etc
    cur = con.cursor()
    insert_data = f"""INSERT INTO {TABLE} (
        logged_date,
        action,
        log_time,
        comment) VALUES (
        '{date.today()}',
        'in',
        '{sys.argv[2]}',
        'ran out of coffee');"""
    cur.execute(insert_data)
    con.commit()
elif sys.argv[1] == "out":
    # OUT
    # Add guard against adding UT after UT - Only allow pattern: IN -> UT -> IN -> UT etc
    cur = con.cursor()
    insert_data = f"""INSERT INTO {TABLE} (
        logged_date,
        action,
        log_time,
        comment) VALUES (
        '{date.today()}',
        'out',
        '{sys.argv[2]}',
        'time to sleep');"""
    cur.execute(insert_data)
    con.commit()
