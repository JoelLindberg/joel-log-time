# Joel's Log Time (shell) app

This app was originally written in Python, but I decided to re-write it in bash as I have a desire to get fluent in bash.

Put the original python cmd line app in the sandbox folder.

# Work notes

## Handling cmd-line args (positional) in bash

Reference and inspiration: https://www.redhat.com/sysadmin/arguments-options-bash-scripts

Later learned there is also something called getopt. Here is my summary of the main and most important differences that helped me to decide (decided on getopts):

* getopt is an external program
* getopts is a bash builtin program
* getopts seems to be more newer and standardized


## SQLite

* https://sqlite.org/download.html
* CLI: https://sqlite.org/cli.html
* https://www.sqlite.org/lang_createtable.html#rowid


### Time in SQLite

https://www.sqlite.org/lang_datefunc.html


date(time-value, modifier, modifier, ...)
time(time-value, modifier, modifier, ...)
datetime(time-value, modifier, modifier, ...)
julianday(time-value, modifier, modifier, ...)
unixepoch(time-value, modifier, modifier, ...)
strftime(format, time-value, modifier, modifier, ...)
timediff(time-value, time-value)



## Database structure

Table log_time:
log_id          INTEGER PRIMARY KEY
logged_date     date                            1970-01-01 00:00:01.000000
action          varchar(3)                      in/out
log_time        varchar(5)                      00:00
comment         varchar(30)
log_state       varchar(4)                      open/done   <- explicitly called - when done is set the sum for the day is re-calculated
PRIMARY KEY     (log_id)

Example day:
in 07 start the day

ut 12 lunch
in 13

ut 15 errand/dog walk
in 16

ut 17 go home

[{23-11-16, 07:00}, {23-11-16, 17:00}]


Table sum_time:
sum_id      INTEGER PRIMARY KEY
sum_date    date
sum         varchar(5)
PRIMARY KEY (sum_id)

