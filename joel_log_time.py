import sys
import os.path
import argparse
import sqlite3
from datetime import datetime
from datetime import timedelta
import re

from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console(tab_size=4)

parser = argparse.ArgumentParser(prog="Joel Log Time console app")
parser.add_argument("-i", "--time-in", help='-i "08:00 2024-07-11"', metavar="time")
parser.add_argument("-o", "--time-out", help='-i "17:00 2024-07-11"', metavar="time")
parser.add_argument("--sum", help="Calculate saldo for all days between the specified date up until todays date", metavar="date")
parser.add_argument("--show", help="Show entries around a specific date", metavar="date")
parser.add_argument("--remove", help="Remove an entry using log_id number", metavar="id")

args = parser.parse_args()


DB_FILE = "joel_log_time.db"
TABLE = "log_time"
TABLE_SUM = "sum_time"
DB_EXISTS = False
TABLE_EXISTS = False
TABLE_SUM_EXISTS = False


# Check if database exists - otherwise create it
# Need to create this for sqlite to check for the database file instead
if os.path.exists(f"./{DB_FILE}"):
    if os.path.isfile(f"./{DB_FILE}") is not True:
        print("Could not create the database: There is a directory named the same as the database that is being created")
else:
    print(f"Creating database: ./{DB_FILE}")

con = sqlite3.connect(f"{DB_FILE}")


# log_time exists? - otherwise create it
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master")
r = cur.fetchall()

for i in r:
    if i[0] == "log_time":
        TABLE_EXISTS = True
        #print(f"Table exists: {i[0]}")

if TABLE_EXISTS == False:
    tables = f"""CREATE TABLE {TABLE} (
        log_id INTEGER PRIMARY KEY,
        logged_date date,
        action varchar(3),
        log_time varchar(5),
        log_state varchar(4),
        comment varchar(30)
        );"""
    # in/out <- 3
    #15:50 <- 5
    cur.execute(tables)
    print("Created table")


# sum_time exists? - otherwise create it
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master")
r = cur.fetchall()

for i in r:
    if i[0] == "sum_time":
        TABLE_SUM_EXISTS = True
        #print(f"Table exists: {i[0]}")

if TABLE_SUM_EXISTS == False:
    tables = f"""CREATE TABLE {TABLE_SUM} (
        sum_id INTEGER PRIMARY KEY,
        sum_date date,
        sum varchar(5)
        );"""
    # in/out <- 3
    #15:50 <- 5
    cur.execute(tables)
    print("Created table")


def validate_log_time(log_time: str) -> list:
    time_date = []
    p1 = "^[0-9]{2}:[0-9]{2}?"
    p2 = "^[0-9]{2}:[0-9]{2} [0-9]{4}-[0-9]{2}-[0-9]{2}?"

    if re.fullmatch(p1, log_time) != None:
        time_date.append(log_time)
        time_date.append(datetime.now().strftime("%Y-%m-%d"))
    elif re.fullmatch(p2, log_time) != None:
        time_date = log_time.split()

    if len(time_date) == 0:
        raise "Something went wrong. Possibly incorrect time and date format entered."

    return time_date


def log_in(log_time: str, log_comment: str):
    '''Adds a time log in the DB for IN events.

    :param log_time: Expects a string like "08:15 2024-06-28".
    Providing a string with only time "08:15" defaults to todays date.
    :param log_comment: A string with any extra info. Empty default.
    '''
    # Add guard against adding IN after IN - Only allow pattern: IN -> UT -> IN -> UT etc

    time_date = validate_log_time(log_time)

    cur = con.cursor()
    insert_query = (f"INSERT INTO {TABLE} ("
        "logged_date,"
        "action,"
        "log_time,"
        "comment) VALUES ("
        f"'{time_date[1]}',"
        "'in',"
        f"'{time_date[0]}',"
        f"\"{log_comment}\");")
    cur.execute(insert_query)
    con.commit()

def log_out(log_time: str, log_comment = ""):
    '''Adds a time log in the DB for OUT events.

    :param log_time: Expects a string like "17:15 2024-06-28".
    Providing a string with only time "17:15" defaults to todays date.
    :param log_comment: A string with any extra info. Empty default.
    '''
    # Add guard against adding OUT after OUT - Only allow pattern: IN -> OUT -> IN -> OUT etc

    time_date = validate_log_time(log_time)

    cur = con.cursor()
    insert_query = (f"INSERT INTO {TABLE} ("
        "logged_date,"
        "action,"
        "log_time,"
        "comment) VALUES ("
        f"'{time_date[1]}',"
        "'out',"
        f"'{time_date[0]}',"
        f"\"{log_comment}\");")
    cur.execute(insert_query)
    con.commit()



def sum_timedeltas(d_timedelta: timedelta) -> timedelta:
    """Addition of timedelta results. Return a single object with the time diffs combined."""
    d_sum = timedelta(seconds=0)
    for d in d_timedelta:
        d_sum = d + d_sum

    return d_sum

def update_sum_time(log_date: str, d_sum: timedelta):
    """Insert or update the table sum_time with a calculated 'saldo' for the specified day.
    : log_date expected to be in format 'yyyy-mm-dd'.
    : d_sum is expected to be a timedelta object containing all the in/out diffs for the specified date."""
    cur = con.cursor()
    cur.execute(f"SELECT sum_id, sum_date FROM sum_time WHERE sum_date = '{log_date}';")
    r = cur.fetchall()

    if len(r) == 1:
        if r[0][1] == log_date:
            print(f"Updating saldo for {log_date}")
            cur.execute(f"""UPDATE {TABLE_SUM} SET sum = '{d_sum}' WHERE sum_id = {r[0][0]};""")
            con.commit()
    elif len(r) > 1:
        print("More than one sum entry for the same date! This needs to be fixed!")
        sys.exit(1)
    else:
        print(f"Created saldo entry for {log_date}.")
        cur.execute(f"""INSERT INTO {TABLE_SUM} (sum_date, sum) VALUES ('{log_date}', '{d_sum}');""")
        con.commit()

def log_sum(log_date: str):
    """Calculate and add saldo for the give date."""
    print(f"Calculating saldo for: {log_date}")

    cur = con.cursor()
    show_data = ("SELECT log_id,"
        "logged_date,"
        "action,"
        "log_time,"
        f"comment FROM {TABLE} "
        f"WHERE logged_date = '{log_date}' ORDER BY log_time ASC;")
    cur.execute(show_data)
    r = cur.fetchall()

    # tmp data structure for calculation - define a model for this?
    logged = []
    for i in r:
        row = {}
        row["log_id"] = i[0]
        row["date"] = i[1]
        row["action"] = i[2]
        row["log_time"] = i[3]
        row["comment"] = i[4]
        logged.append(row)

    # calculate/create diffs (timedeltas) between in and out log events
    dates = []
    d_timedelta = []
    previous_action = ""
    idx = 0
    for i in logged:
        #print(f'calcdbg: {i["date"]}, {i["log_time"]}, {i["action"]}')
        dates.append(datetime.fromisoformat(f'{str(i["date"])}T{i["log_time"]}'))

        if i["action"] == "out" and previous_action == "in":
            d_timedelta.append(dates[idx] - dates[idx - 1])
            previous_action = "out"
        elif i["action"] == "in" and previous_action == "in":
            raise ValueError("Incorrect time log event order logged. 'in' is followed by 'in'.")
        elif i["action"] == "out" and previous_action == "out":
            raise ValueError("Incorrect time log event order logged. 'out' is followed by 'out'.")
        elif i["action"] == "in":
            previous_action = "in"
        idx += 1

    # sum the diffs
    d_sum = sum_timedeltas(d_timedelta)
    # Sum old data into table sum_time - update if it exists
    update_sum_time(log_date, d_sum)



def log_show(log_date = ""):
    """Show entries ordered by time.
    Also shows some days before and after for convenience.
    A specific origin date can be set."""
    if log_date == "":
        log_datetime = datetime.now()
    else:
        log_datetime = datetime.fromisoformat(log_date)

    before = (log_datetime - timedelta(days=15)).strftime("%Y-%m-%d")
    after = (log_datetime + timedelta(days=15)).strftime("%Y-%m-%d")

    # Don't allow "after" to be set in the future
    if after > datetime.now().strftime("%Y-%m-%d"):
        after = datetime.now().strftime("%Y-%m-%d")

    show_data = ("SELECT log_id,"
        "logged_date,"
        "action,"
        "log_time,"
        f"comment FROM {TABLE} "
        f"WHERE logged_date >= '{before}' AND logged_date <= '{after}' ORDER BY logged_date, log_time;")
    cur = con.cursor()
    cur.execute(show_data)
    r = cur.fetchall()

    table = Table(title=f"Entries between {before} and {after}")
    table.add_column("id", justify="right", style="cyan", no_wrap=True)
    table.add_column("action", style="blue")
    table.add_column("time", style="magenta")
    table.add_column("logged_date", justify="right", style="green")
    table.add_column("comment", justify="right", style="green")

    for l in r:
        table.add_row(str(l[0]), str(l[2]), str(l[3]), str(l[1]), str(l[4]))
        #print(l)
    
    #console = Console()
    console.print(table)
    


    


def log_remove(log_id: int):
    """Remove a logged time entry."""
    cur = con.cursor()
    cur.execute(f"DELETE FROM {TABLE} WHERE log_id = '{log_id}';")
    con.commit()

def saldo():
    cur = con.cursor()
    show_data = f"SELECT sum FROM {TABLE_SUM}"
    cur.execute(show_data)
    r = cur.fetchall()
    s = timedelta(seconds=0)
    expected_hours = 0
    for day_saldo in r:
        s_split = day_saldo[0].split(":")
        s = s + timedelta(seconds=int(s_split[2]), minutes=int(s_split[1]), hours=int(s_split[0]))
        # Expected hours to have worked based on logged entries
        expected_hours += 8

    print(f"You have worked: {s} hours")
    print(f"Expected work: {expected_hours} hours")
    saldo = (timedelta(hours=expected_hours) - s).total_seconds()
    print(f"Saldo (in seconds): {saldo}")
    if saldo < 0:
        console.print(f"Saldo: -{timedelta(seconds=abs(saldo))}", style="cyan")
    else:
        text = Text(f"Saldo: {timedelta(seconds=saldo)}")
        text.stylize("red")
        console.print(text)


def main():
    if args.sum and (args.time_in != None or args.time_out != None or args.remove != None):
        print("Not allowed to calculate sum while adding time. Sum must be run separately.")
        sys.exit(1)

    if args.time_in != None:
        log_in(args.time_in, "Coffee up and let's work!")
    elif args.time_out != None:
        log_out(args.time_out, "Remember why you work hard. Let's go home!")
    elif args.sum == True:
        log_sum(args.sum)
    elif args.show != None:
        log_show(args.show)
    elif args.remove != None:
        log_remove(args.remove)
    else:
        log_show()
        saldo()
        print("\n")
        parser.print_help()


if __name__ == "__main__":
    main()
