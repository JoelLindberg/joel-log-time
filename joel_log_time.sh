#!/bin/bash


# Check if sqlite3 installed and the version

sqlite_installed=$(sqlite3 -version)

if [ $? -eq 127 ];
then
   echo "sqlite3 was not found. It must be installed for this utility to work."
   exit
fi

sqlite_version=$(echo $sqlite_installed | grep -Eow "3.41.[0-9]+")

if [ "${#sqlite_version}" -eq 0 ];
then
   echo "Warning: sqlite3 version 3.41.x is not used. It is the only version this tool has been tested with."
   echo
fi


# Database items

log_database="workwork.db"
logged_time="logged_time"
worked_hours="worked_hours"

# Check if the tables exist - otherwise create them

create_logged_time=$(echo "CREATE TABLE $logged_time (\
log_id INTEGER PRIMARY KEY,\
logged_date date,\
action varchar(3),\
log_time varchar(5),\
log_state varchar(4),\
comment varchar(30)\
);")

create_worked_hours="CREATE TABLE $worked_hours (\
sum_id INTEGER PRIMARY KEY,\
sum_date date,\
sum varchar(5)\
);"

logged_time_exists=$(sqlite3 ${log_database} .tables | grep -Eow "$logged_time")

if [ -z $logged_time_exists ];
then
   sqlite3 $log_database "$create_logged_time"
fi

worked_hours_exists=$(sqlite3 ${log_database} .tables | grep -Eow "$worked_hours")

if [ -z $worked_hours_exists ];
then
   sqlite3 $log_database "$create_worked_hours"
fi


# Menu methods

Help() {
   # Display help
   echo "🐢 Joel's Log Time"
   echo
   echo "Log your work time using this simple shell app."
   echo "Logged time data is stored in an sqlite database in this directory."
   echo
   echo "Syntax: scriptTemplate [-i|o|e|s]"
   echo "options:"
   echo "i     Date and time In (example: -i 2024-01-07T08:30)."
   echo "o     Date and time Out example: -o 2024-01-07T17:30."
   echo "e     End day by recording total work hours for the day."
   echo "s     Show saldo for all logged time entries."
   echo
}

In() {
   # Log In timestamp
   echo $1

   IFS="T"
   read -a datetime_split <<< $1
   echo "Date entered: ${datetime_split[0]}"
   echo "Time entered: ${datetime_split[1]}"
   unset IFS
}

Out() {
   # Log Out timestamp
   echo $1

   IFS="T"
   read -a datetime_split <<< $1
   echo "Date entered: ${datetime_split[0]}"
   echo "Time entered: ${datetime_split[1]}"
   unset IFS
}

Sum() {
   # Record total worked hours for the day
   echo "Sum"
}

Saldo() {
   # Show total saldo for all recorded days
   echo "Saldo"
}


# Helper methods

ValidateDatetime() {
   # Validate date and time
   # Shorter version of ISO 8601 date (2004-02-12T15:19:21+00:00) -> 20023-11-05T08:30
   # Example: 2024-01-07T14:51
   datetime_valid=$(echo $1 | grep -E -w "^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])T(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")

   if [ -z $datetime_valid ];
   then
      echo "Invalid input datetime format: $1"
      echo "Valid format example: 2024-01-07T08:30"
      exit
   fi
}

ValidateDate() {
   # Validate date
   # Example: 2024-01-07
   date_valid=$(echo $1 | grep -E -w "^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])$")

   if [ -z $date_valid ];
   then
      echo "Invalid input date format: $1"
      echo "Valid format example: 2024-01-07"
      exit
   fi
}


# Database methods

# TODO:

# input date and/or time to epoch time
# https://stackoverflow.com/questions/10990949/convert-date-time-string-to-epoch-in-bash
date --date '18:00' +"%s"

#sqlite3 test.db 'select * from drinks'

# timedelta: diff epoch time between epoch timestamps

# sum timedeltas and save the result for the day in worked_hours





# Show help (menu) if no args are given

if [ -z $1 ];
then
   Help
   exit
fi

while getopts "i:o:e:sh" option; do
   case $option in
      i)
         # Log an In time entry
         # Requires <date>
         # 2023-10-22T07:30
         ValidateDatetime $OPTARG
         In $OPTARG
         exit;;
      o)
         # Log an Out time entry
         # Requires <date>
         # 2023-10-22T07:30
         ValidateDatetime $OPTARG
         Out $OPTARG
         exit;;
      e)
         # End the day and sum all time entries
         # Requires <date>
         # 2023-10-22
         ValidateDate $OPTARG
         echo "sum"
         Sum
         exit;;
      s)
         # Show current saldo for all time entries
         echo "saldo"
         Saldo
         exit;;
      h)
         Help
         exit;;
      *)
         echo "Missing arguments or required argument value. Have a look at what's being served:"
         echo
         Help
         exit;;
   esac
done
