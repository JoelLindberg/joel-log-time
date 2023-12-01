# joel_log_time app

Python SQLite:

https://docs.python.org/3/library/sqlite3.html

*"The sqlite3 module was written by Gerhard Häring. It provides an SQL interface compliant with the DB-API 2.0 specification described by PEP 249"*

Python MySQL:

Apparently this driver is following the Python DB API 2.0 standard referenced above. This makes SQLite and MySQL very interchangeable for Python.

https://dev.mysql.com/doc/refman/8.0/en/apis-python.html


## sqlite

I will go with sqlite for now. Since both the mysql driver and python's sqlite library use the same Python DB 2.0 API it should be easy to switch later. I could also program some kind of encapsulation with an interface to allow an easy update later if I want to move to MySQL.

* https://sqlite.org/download.html
* https://sqlite.org/cli.html
* https://docs.python.org/3/library/sqlite3.html
* https://www.sqlite.org/lang_createtable.html#rowid



Table log_time:
log_id          INTEGER PRIMARY KEY
logged_date     date                            1970-01-01 00:00:01.000000
action          varchar(3)                      data: in/out
log_time        varchar(5)
comment         varchar(30)
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
